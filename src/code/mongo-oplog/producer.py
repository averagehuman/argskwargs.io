
import os
import random
import signal

from bson.timestamp import Timestamp
import redis
import gevent
import gevent.queue
import gevent.fileobject
import gevent.monkey
import pymongo
    
import config as cfg


def random_wait():
    """
    Simulate_work.
    """
    gevent.sleep(random.random())


def bson_ts_to_long(timestamp):
    """Convert BSON timestamp into integer.

    Conversion rule is based from the specs
    (http://bsonspec.org/#/specification).
    """
    return ((timestamp.time << 32) + timestamp.inc)


def long_to_bson_ts(val):
    """Convert integer into BSON timestamp.
    """
    seconds = val >> 32
    increment = val & 0xffffffff

    return Timestamp(seconds, increment)


MONGO_CONNECTION_FAILURE = (
    pymongo.errors.AutoReconnect,
    pymongo.errors.OperationFailure,
    pymongo.errors.ConfigurationError
)

class OplogTail:

    def __init__(self, client, processor, namespace=None, buffer=200, batch=50, workers=1, lazy=5, stash=None):
        assert workers > 0, "There must be at least one worker"
        self.oplog = client.local.oplog.rs
        self.processor = processor
        self.namespace = namespace
        self.stash = stash or os.path.join(
            os.getcwd(), ((namespace or '') + '.oplog.tmp').lstrip('.')
        )
        self.batchsize = batch
        self.lazy = lazy
        self._pending = gevent.queue.Queue(buffer)
        self._threads = [ gevent.spawn(self._buffer) ]
        for _ in range(workers):
            self._threads.append(gevent.spawn(self._process))

    def _last_processed_timestamp(self):
        latest = self.processor.timestamp()
        if latest:
            return long_to_bson_ts(latest)

    def _last_oplog_timestamp(self):
        """
        Return the timestamp of the latest entry in the oplog.
        """
        if not self.namespace:
            cursor = self.oplog.find()
        else:
            cursor = self.oplog.find({'ns': {'$in': self.namespace}})

        try:
            # use limit(-1) to return at most 1 item
            ts = next(cursor.sort('$natural', pymongo.DESCENDING).limit(-1))['ts']
        except StopIteration:
            ts = None

        return ts

    def _get_oplog_cursor(self):
        """
        Get a cursor to the oplog.

        Filter by namespace, if one is given.
        
        If the processor returns a value for returns a cursor to the entire oplog.
        """
        query = {}

        if self.namespace:
            query['ns'] = {'$in': self.namespace}

        timestamp = self._last_processed_timestamp()

        if timestamp:
            query['ts'] = {'$gte': timestamp}

        cursor = self.oplog.find(query, cursor_type=pymongo.CursorType.TAILABLE_AWAIT)

        if timestamp:
            # Applying 8 as the mask to the cursor enables OplogReplay
            cursor.add_option(8)

        try:
            cursor.clone().limit(-1)[0]
        except (IndexError, pymongo.errors.AutoReconnect):
            cursor = None
        return cursor

    def _buffer(self):
        while True:
            while not self._pending.empty():
                print('BUFFER:    Waiting for current buffer to be processed before reconnecting to mongo')
                gevent.sleep(self.lazy)
            print("BUFFER:    Getting oplog cursor.")
            cursor = self._get_oplog_cursor()
            if not cursor:
                print("BUFFER:    Either could not connect to database or local.oplog.rs is empty. Retrying in 5s...")
                gevent.sleep(5)
                continue
            try:
                while cursor.alive:
                    for entry in cursor:

                        # Don't replicate entries resulting from chunk moves
                        if entry.get("fromMigrate"):
                            continue

                        # Sync the current oplog operation
                        operation = entry['op']
                        ns = entry['ns']

                        if '.' not in ns:
                            continue
                        coll = ns.split('.', 1)[1]

                        # Ignore system collections
                        if coll.startswith("system."):
                            continue

                        # Ignore GridFS chunks
                        if coll.endswith('.chunks'):
                            continue

                        timestamp = bson_ts_to_long(entry['ts'])
                        print("BUFFER:    Buffering oplog entry ts='%s'" % entry['ts'])
                        self._pending.put_nowait((timestamp, entry))
                        gevent.sleep(0)
                    print('BUFFER:    Mongodb cursor is alive but has no data')
                    gevent.sleep(3)
            except MONGO_CONNECTION_FAILURE as err:
                print("BUFFER:    Cursor closed due to an exception - %s" % err)
            except gevent.queue.Full:
                print('BUFFER:    Buffer is full. Backing off.')
            del cursor
            gevent.sleep(2)

    def _process(self):
        rng = range(self.batchsize)
        while True:
            payload = []
            try:
                for idx in rng:
                    ts, entry = self._pending.get(block=True, timeout=self.lazy)
                    gevent.sleep(0)
                    payload.append((ts, entry))
            except gevent.queue.Empty:
                pass
            if payload:
                print('PROCESSOR: Processing %d items' % len(payload))
                self.processor.process(payload)
            else:
                print("PROCESSOR: Worker thread '%s' is waiting for data..." % id(gevent.getcurrent()))
            gevent.sleep(self.lazy)
            
    def shutdown(self):
        print('Shutting down')

    def join(self):
        gevent.joinall(self._threads)

class FileOutProcessor(gevent.fileobject.FileObjectThread):

    def __init__(self, filepath):
        super().__init__(open(filepath, 'a'))
        self._timestamp = None

    def timestamp(self):
        return self._timestamp

    def process(self, items):
        for ts, doc in items:
            self.io.write(str(doc) + '\n')
            self._timestamp = ts

    def __enter__(self):
        return self

    def __exit__(self, objtype, value, traceback):
        self.close()


def main():
    dbname = cfg.EVE_SETTINGS['MONGO_DBNAME']
    client = pymongo.MongoClient(cfg.EVE_SETTINGS['MONGO_HOST'], cfg.EVE_SETTINGS['MONGO_PORT'])
    gevent.signal(signal.SIGQUIT, gevent.kill)
    with FileOutProcessor('oplog.log') as fileout:
        tail = OplogTail(client, fileout)
        try:
            tail.join()
        except KeyboardInterrupt:
            print('Program Exit.')


if __name__ == '__main__':
    gevent.monkey.patch_all()
    try:
        main()
    except KeyboardInterrupt:
        pass



import os
import random
import signal

from bson.timestamp import Timestamp
import redis
import gevent
import gevent.queue
import pymongo
import faker
    
import config as cfg

fake = faker.Faker(cfg.FAKER_LOCALE)

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


class OplogBatchProcessor:

    def __init__(self, db, processor, namespace=None, buffer=50, batch=10, rundir=os.getcwd()):
        self.oplog = db.local.oplog.rs
        self.processor = processor
        self.namespace = namespace
        self.rundir = rundir
        self.timestamp_file = os.path.join(
            rundir, (namespace or 'oplog').strip('.') + '.ts'
        )
        self.batch_size = batch
        self._pending = gevent.queue.Queue(buffer)

    def run(self):
        gevent.signal(signal.SIGQUIT, gevent.kill)
        threads = [
            gevent.spawn(self._buffer),
            gevent.spawn(self._process),
            gevent.spawn(self._process),
        ]
        try:
            gevent.joinall(threads)
        except:
            self._shutdown()
            raise


    def _shutdown(self):
        print('Shutting down')

    def _buffer(self):
        while True:
            while not self._pending.empty():
                print('Waiting for current buffer to be processed before reconnecting to mongo')
                gevent.sleep(2)
            while True:
                random_wait()
                word = fake.word()
                try:
                    print("Putting '%s'" % word)
                    self._pending.put(word, block=False)
                except gevent.queue.Full:
                    print("Buffer is full. Waiting for tasks to complete.")
                    gevent.sleep(2)


    def _process(self):
        rng = range(self.batch_size)
        while True:
            payload = []
            try:
                for idx in rng:
                    word = self._pending.get(block=True, timeout=1.5)
                    print("Got '%s'" % word)
                    payload.append(word)
            except gevent.queue.Empty:
                pass
            if payload:
                print('batching %s' % payload)
                random_wait()
            else:
                print("No new data. Processor thread '%s' is sleeping for 1s" % id(gevent.getcurrent()))
                gevent.sleep(1)
            

    def get_last_timestamp(self):
        value = None
        if os.path.exists(self.timestamp_file):
            with open(self.timestamp_file) as fileobj:
                value = long_to_bson_ts(int(fileobj.read().strip()))
        return value

    def set_last_timestamp(self, value):
        with open(self.timestamp_file, 'w') as fileobj:
            fileobj.write(str(bson_ts_to_long(value)))

    def get_current_timestamp(self):
        if self.namespace:
            query = self.oplog.find({'ns': {'$in': self.namespace}})
        else:
            query = self.oplog.find()
        # use limit(-1) to return at most 1 item
        query = query.sort('$natural', pymongo.DESCENDING).limit(-1)

        if query.count(with_limit_and_skip=True) == 0:
            return None

        return query[0]['ts']


def main():
    dbname = cfg.EVE_SETTINGS['MONGO_DBNAME']
    client = pymongo.MongoClient(cfg.EVE_SETTINGS['MONGO_HOST'], cfg.EVE_SETTINGS['MONGO_PORT'])
    db = client[dbname]
    queue = redis.StrictRedis()
    oplog_processor = OplogBatchProcessor(db, queue)
    oplog_processor.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass


"""
MongoDB Create/Update/Delete activity simulator.

+ Runs a python-eve/flask HTTP server as a REST interface to the database. 
+ Runs separate green threads that loop continuously, randomly creating,
  updating and deleting.

Usage: python source.py

Ctrl-C to stop.

Lowering ACTIVITY_MAX_WAIT will increase the request rate.

Requires:  gevent, python-eve and fake-factory.
Tested on: Python 3.4
"""

import json
import random
from datetime import datetime

import grequests # calls gevent.monkey.patch_all(thread=False, select=False)
import gevent
import gevent.wsgi
import pymongo
import eve
import faker

import config as cfg

# cache of (userid, etag) pairs
USER_SET = set()

#----------------------------------------------------------------------------------------
# Utilities
#----------------------------------------------------------------------------------------
fake = faker.Faker(cfg.FAKER_LOCALE)


def fake_user_tags():
    """
    Generate a list of HTML colour names to represent a list of tags.
    """
    return [fake.color_name().lower() for _ in range(0, random.randint(0, 10))]


def fake_user_data():
    """
    Use the fake-factory lib to create real-looking user data matching the mongo schema.
    """
    fname = fake.first_name()
    lname = fake.last_name()
    email = '%s.%s@mail.localhost' % (fname.lower(), lname.lower())
    return {
        'fname': fname,
        'lname': lname,
        'email': email,
        'username': fake.user_name(),
        'dob': fake.date_time().strftime(cfg.EVE_SETTINGS['DATE_FORMAT']),
        'tags': fake_user_tags(),
        'location': {
            'address': fake.street_address(),
            'city': fake.city(),
        },
    }


def fake_user_update():
    """
    Generate fake update for an existing user.
    """
    probability = cfg.UPDATE_LIKELIHOOD / 3.0
    payload = {}
    if random.random() < probability:
        payload['email'] =  '%s.%s@mail.localhost' % (fake.word(), fake.word())
    if random.random() < probability:
        payload['tags'] = fake_user_tags()
    if random.random() < probability:
        payload['location'] = {'address': fake.street_address()}
    return payload


def on_request_error(request, exception):
    print(exception)
    

def create_users(count):
    """
    Bulk create users via async HTTP requests to the Eve server.
    """
    def irequests():
        for _ in range(count):
            fake_data = json.dumps(fake_user_data())
            yield grequests.post(cfg.USER_CREATE_URL, data=fake_data, headers=cfg.HEADERS)
    for response in grequests.map(irequests(), exception_handler=on_request_error):
        try:
            content = response.content.decode('utf8')
            data = json.loads(content)
        except Exception as err:
            print("Error parsing JSON response - %s" % err)
            continue
        else:
            status = data.get('_status')
            userid = data.get('_id')
            etag = data.get('_etag', '')
            if status != 'OK' or not userid:
                print("Unexpected response - %s" % content)
            else:
                USER_SET.add((userid, etag))
                print("Created user '%s'" % userid)


def find_existing_dataset(db):
    """
    If the users collection is non-empty populate the USER_SET cache with any users found.
    """
    for user in db.users.find():
        userid = str(user.get('_id', ''))
        if userid:
            etag = user.get('_etag', '')
            USER_SET.add((userid, etag))
    existing = len(USER_SET)
    if existing > 0:
        print('Found %d existing users' % existing)


def create_indexes(db):
    """
    Create indexes on mongodb collections for better query performance.
    """
    # username is unique in users collection
    db.users.create_index([('username', pymongo.ASCENDING)], unique=True)


def random_wait(lower=0, upper=cfg.ACTIVITY_MAX_WAIT):
    """
    Sleep for a random number of seconds. No shorter than lower and no longer than upper.
    """
    gevent.sleep(random.randint(lower, upper))


#----------------------------------------------------------------------------------------
# Greenlets
#----------------------------------------------------------------------------------------
def activity_logger(db):
    """
    Print out an activity summary.
    """
    while True:
        usercount = db.users.count()
        timestamp = datetime.now().strftime(cfg.EVE_SETTINGS['DATE_FORMAT'])
        msg = 'There are %s (%s) users on %s' % (usercount, len(USER_SET), timestamp)
        print(msg)
        gevent.sleep(cfg.ACTIVITY_STATUS_WAIT)


def populate():
    """
    If no initial data set is found, create one here.

    Users are created via batches of async POSTs to the Eve server with 'MAX_CONCURRENCY'
    requests in each batch.
    """
    factor, remainder = divmod(cfg.USER_INITIAL_POPULATION, cfg.MAX_CONCURRENCY)
    for _ in range(factor):
        create_users(cfg.MAX_CONCURRENCY)
        gevent.sleep(1)
    if remainder:
        create_users(remainder)


def create():
    """
    Continuously create new users.
    """
    while True:
        if random.random() < cfg.CREATE_LIKELIHOOD:
            create_users(1)
        random_wait()


def update():
    """
    Continuously update existing users at random.
    """
    while True:
        if USER_SET and random.random() < cfg.DELETE_LIKELIHOOD:
            # select an existing user at random and send a PATCH request with a fake update.
            userid, etag = random.choice(list(USER_SET))
            url = cfg.USER_ENDPOINT_PATTERN % userid
            headers = dict(cfg.HEADERS)
            fake_data = fake_user_update()
            if etag:
                headers['If-Match'] = etag
            data = fake_user_update()
            # Update data is generated at random and may be empty.
            # An empty payload is a no-op but ignore in any case.
            if data:
                payload = json.dumps(data)
                request = grequests.patch(url, data=payload, headers=headers)
                request.send()
                if request.response.status_code >= 400:
                    print(request.response.content)
                else:
                    # Need to update cached etag
                    response = json.loads(request.response.content.decode('utf8'))
                    newtag = response['_etag']
                    USER_SET.remove((userid, etag))
                    USER_SET.add((userid, newtag))
                    print("Updated user '%s'. Payload -> %s" % (userid, payload))
        random_wait()


def delete():
    """
    Continuously delete existing users at random.
    """
    while True:
        if USER_SET and random.random() < cfg.DELETE_LIKELIHOOD:
            # select an existing user at random and send a DELETE request
            userid, etag = random.choice(list(USER_SET))
            url = cfg.USER_ENDPOINT_PATTERN % userid
            headers = dict(cfg.HEADERS)
            if etag:
                headers['If-Match'] = etag
            request = grequests.delete(url, headers=headers)
            request.send()
            if request.response.status_code >= 400:
                print(request.response.content)
            else:
                try:
                    USER_SET.remove((userid, etag))
                except KeyError:
                    pass
                print("Deleted user '%s'." % userid)
        random_wait()


#----------------------------------------------------------------------------------------
# Main function
#----------------------------------------------------------------------------------------
def main():
    client = pymongo.MongoClient(cfg.EVE_SETTINGS['MONGO_HOST'], cfg.EVE_SETTINGS['MONGO_PORT'])
    db = client[cfg.EVE_SETTINGS['MONGO_DBNAME']]

    create_indexes(db)
    find_existing_dataset(db)

    app = eve.Eve(settings=cfg.EVE_SETTINGS)
    server = gevent.wsgi.WSGIServer(cfg.SERVER_ADDRESS, app)

    threads = [
        gevent.spawn(server.serve_forever),
        gevent.spawn(activity_logger, db),
        gevent.spawn_later(cfg.ACTIVITY_INITIAL_DELAY, create),
        gevent.spawn_later(cfg.ACTIVITY_INITIAL_DELAY, update),
        gevent.spawn_later(cfg.ACTIVITY_INITIAL_DELAY, delete),
    ]

    if not USER_SET:
        threads.append(gevent.spawn(populate))

    try:
        gevent.joinall(threads)
    except KeyboardInterrupt:
        server.stop()
        gevent.killall(threads)


if __name__ == '__main__':
    main()


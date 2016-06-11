"""
MongoDB Create/Update/Delete activity simulator.

Requires: gevent, python-eve and fake-factory.
"""

import json
import random
from datetime import datetime

import grequests
import gevent
import gevent.monkey
import gevent.wsgi
import pymongo
import eve
import faker
from faker.providers.color import Provider as FakeColorProvider


SERVER_ADDRESS = ('127.0.0.1', 5000)
HEADERS = {'Content-Type': 'application/json'}
FAKER_LOCALE = 'en_GB'
MAX_CONCURRENCY = 50

# activity parameters
ACTIVITY_INITIAL_DELAY = 4   # delay before create/update/delete activity begins
ACTIVITY_MAX_WAIT = 5        # upper limit to waits between creates/updates/deletes
ACTIVITY_STATUS_WAIT = 3     # wait between status messages
CREATE_LIKELIHOOD = 0.4
DELETE_LIKELIHOOD = 0.3
UPDATE_LIKELIHOOD = 0.4

# user api
USER_SET = set()
USER_INITIAL_POPULATION = 100
USER_CREATE_URL = 'http://%s:%s/users/' % SERVER_ADDRESS
USER_ENDPOINT_PATTERN = USER_CREATE_URL + '%s'

COLOURS = [colour.lower() for colour in FakeColorProvider.all_colors.keys()]

PERSON = {
    'fname': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 20,
        'required': True,
    },
    'lname': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 25,
        'required': True,
    },
    'username': {
        'type': 'string',
        'minlength': 1,
        'maxlength': 30,
        'required': True,
        'unique': True,
    },
    'email': {
        'type': 'string',
        'maxlength': 50,
        'required': True,
        'unique': True,
    },
    'dob': {
        'type': 'datetime',
    },
    # 'tags' is a list, and can only contain values from 'allowed'.
    'tags': {
        'type': 'list',
        'allowed': COLOURS
    },
    # An embedded 'strongly-typed' dictionary.
    'location': {
        'type': 'dict',
        'schema': {
            'address': {'type': 'string'},
            'city': {'type': 'string'}
        },
    },
}

EVE_SETTINGS = dict(
    MONGO_HOST='localhost',
    MONGO_PORT=27017,
    MONGO_DBNAME='mctest',
    DOMAIN={
        'users': {
            'schema': PERSON,
            'resource_methods': ['GET', 'POST'],
            'item_methods': ['GET', 'PATCH', 'PUT', 'DELETE'],
            'additional_lookup': {
                'url': 'regex("[-\w]+")',
                'field': 'username'
            },
        }
    },
    DATE_FORMAT='%a, %d %b %Y %H:%M:%S',
    OPLOG=True,
)



#----------------------------------------------------------------------------------------
# Utilities
#----------------------------------------------------------------------------------------
fake = faker.Faker(FAKER_LOCALE)


def fake_user_tags():
    """
    Generate a list of HTML colour names to represent a list of tags.
    """
    return [fake.color_name().lower() for _ in range(0, random.randint(0, 10))]


def generate_fake_user_data():
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
        'dob': fake.date_time().strftime(EVE_SETTINGS['DATE_FORMAT']),
        'tags': fake_user_tags(),
        'location': {
            'address': fake.address(),
            'city': fake.city(),
        },
    }


def on_request_error(request, exception):
    print(exception)
    

def create_users(count):
    """
    Bulk create users via async HTTP requests to the Eve server.
    """
    def irequests():
        for _ in range(count):
            fake_data = generate_fake_user_data()
            yield grequests.post(USER_CREATE_URL, data=json.dumps(fake_data), headers=HEADERS)
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
                print(content)



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


def random_wait():
    gevent.sleep(random.randint(0, ACTIVITY_UPPER_DELAY))


#----------------------------------------------------------------------------------------
# Greenlets
#----------------------------------------------------------------------------------------
def activity_logger(db):
    """
    Print out an activity summary.
    """
    while True:
        usercount = db.users.count()
        timestamp = datetime.now().strftime(EVE_SETTINGS['DATE_FORMAT'])
        msg = 'There are %s (%s) users at %s' % (usercount, len(USER_SET), timestamp)
        print(msg)
        gevent.sleep(ACTIVITY_STATUS_WAIT)


def populate():
    """
    If no initial data set is found, create one here.

    Users are created via batches of async POSTs to the Eve server with 'MAX_CONCURRENCY'
    requests in each batch.
    """
    factor, remainder = divmod(USER_INITIAL_POPULATION, MAX_CONCURRENCY)
    for _ in range(factor):
        create_users(MAX_CONCURRENCY)
        gevent.sleep(1)
    if remainder:
        create_users(remainder)


def create():
    """
    Create new users.
    """
    while True:
        if random.random() < CREATE_LIKELIHOOD:
            create_users(1)
        random_wait()


def update():
    """
    Update existing users.
    """
    pass


def delete():
    """
    Delete existing users.
    """
    while True:
        if USER_SET and random.random() < DELETE_LIKELIHOOD:
            userid, etag = random.choice(list(USER_SET))
            headers = dict(HEADERS)
            if etag:
                headers['If-Match'] = etag
            url = USER_ENDPOINT_PATTERN % userid
            request = grequests.delete(url, headers=headers)
            request.send()
            if request.response.status_code >= 400:
                print(request.response.content)
            else:
                try:
                    USER_SET.remove((userid, etag))
                except KeyError:
                    pass
        random_wait()


#----------------------------------------------------------------------------------------
# Main function
#----------------------------------------------------------------------------------------
def main():
    client = pymongo.MongoClient(EVE_SETTINGS['MONGO_HOST'], EVE_SETTINGS['MONGO_PORT'])
    db = client[EVE_SETTINGS['MONGO_DBNAME']]

    create_indexes(db)
    find_existing_dataset(db)

    app = eve.Eve(settings=EVE_SETTINGS)
    server = gevent.wsgi.WSGIServer(SERVER_ADDRESS, app)

    threads = [
        gevent.spawn(server.serve_forever),
        gevent.spawn(activity_logger, db),
        gevent.spawn_later(ACTIVITY_INITIAL_DELAY, create),
        gevent.spawn_later(ACTIVITY_INITIAL_DELAY, delete)
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


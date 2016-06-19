
from faker.providers.color import Provider as FakeColorProvider

SERVER_ADDRESS = ('127.0.0.1', 5000)
HEADERS = {'Content-Type': 'application/json'}
FAKER_LOCALE = 'en_GB'
MAX_CONCURRENCY = 50

# activity parameters
ACTIVITY_INITIAL_DELAY = 4   # delay before create/update/delete activity begins
ACTIVITY_MAX_WAIT = 3        # upper limit to waits between creates/updates/deletes
ACTIVITY_STATUS_WAIT = 3     # wait between status messages
CREATE_LIKELIHOOD = 0.4
DELETE_LIKELIHOOD = 0.3
UPDATE_LIKELIHOOD = 0.4

# user api
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



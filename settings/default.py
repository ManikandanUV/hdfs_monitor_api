import logging
import os
import sys

DEBUG = True

LOGGING = dict(
    version=1,
    disable_existing_loggers=False,
    formatters={
        'stamped': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        },
    },
    handlers={
        'syslog': {
            'level': 'NOTSET',
            'class': 'logging.handlers.SysLogHandler',
            'address': '/var/run/syslog' if sys.platform == 'darwin' else '/dev/log',
            'facility': logging.handlers.SysLogHandler.LOG_LOCAL1,
            'formatter': 'stamped',
        },
        'console': {
            'level': 'NOTSET',
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'stamped',
        },
    },
    loggers={
        '': {
            'handlers': ['console', 'syslog'],
            'level': 'INFO',
            'propagate': True,
        }
    }
)

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the API server
API_SERVER = os.environ.get('API_SERVER')

# Define API Access token
API_TOKEN = os.environ.get('API_TOKEN')

# Define Postgres credentials
PG_USER = os.environ.get('PG_USER')
PG_PASSWORD = os.environ.get('PG_PASSWORD')
PG_HOST = os.environ.get('PG_HOST')
TEST_USER = os.environ.get('TEST_USER')
TEST_PASSWORD = os.environ.get('TEST_PASSWORD')

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join('/home/mramakri/', 'hdfs_monitor.db')
# SQLALCHEMY_DATABASE_URI = 'postgresql://' + PG_USER + ':' + PG_PASSWORD + '@' + PG_HOST + ':5432/audience_db'
DATABASE_CONNECT_OPTIONS = {}

# Define Hbase server
HBASE_THRIFT_SERVER = 'dev-hadoopmg02.client.ext'


# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

SNS_PALETTE = ['#4c72b0', '#55a868', '#c44e52', '#8172b2', '#ccb974', '#64b5cd']
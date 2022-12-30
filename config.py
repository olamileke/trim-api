
from os import path, environ

DEBUG = False
TESTING = False
CSRF_ENABLED = False
BASE_DIR = path.abspath(path.dirname(__file__))
BUNDLE_ERRORS = True
DB_USER = environ.get('DB_USER')
DB_PASSWORD = environ.get('DB_PASSWORD')
DB_HOST = environ.get('DB_HOST')
DB_PORT = environ.get('DB_PORT')
DB_NAME = environ.get('DB_NAME')
SECRET_KEY = environ.get('SECRET_KEY')
CLIENT_URL = environ.get('CLIENT_URL')
MAIL_BASE_URL = environ.get('MAIL_BASE_URL')
MAIL_API_KEY = environ.get('MAIL_API_KEY')
MAIL_FROM = environ.get('MAIL_FROM')
MAIL_FROM_URL = environ.get('MAIL_FROM_URL')
PER_PAGE = environ.get('PER_PAGE')

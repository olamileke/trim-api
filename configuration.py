import os.path as path

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    BASE_DIR = path.abspath(path.dirname(__file__))
    BUNDLE_ERRORS = True
    DB_USER = ''
    DB_PASSWORD = ''
    DB_PORT = ''
    DB_NAME = '' 
    SECRET_KEY = ''
    CLIENT_URL = ''       
    MAIL_BASE_URL = ''
    MAIL_API_KEY = ''
    MAIL_FROM = ''
    MAIL_FROM_URL = ''
    PER_PAGE = 6
    S3_BUCKET = ''
    S3_BUCKET_LINK = ''
    S3_ACCESS_KEY_ID = ''
    S3_SECRET_KEY = ''

class DevelopmentConfig(Config):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = True 
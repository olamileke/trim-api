import os.path as path

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    BASE_DIR = path.abspath(path.dirname(__file__))
    BUNDLE_ERRORS = True
    DB_USER = 'olamileke'
    DB_PASSWORD = 'Arsenalfc1886'
    DB_PORT = 'trim.crpnavrugexe.us-east-2.rds.amazonaws.com:5432'
    DB_NAME = 'postgres'
    SECRET_KEY = 'mYYP2dJBNeyclufoYuEJ'
    CLIENT_URL = 'https://trimapp.netlify.app'
    MAIL_BASE_URL = "https://api.mailgun.net/v3/sandboxb3e06f45528541edbc677fe253ca0c00.mailgun.org/messages"
    MAIL_API_KEY = "key-618e6125c452b712ee91e57f028fbd0f"
    MAIL_FROM = "Trim"
    MAIL_FROM_URL = "<admin@trimm.in>"
    PER_PAGE = 6
    S3_BUCKET = 'thetrimappbucket'
    S3_BUCKET_LINK = 'https://s3-us-east-2.amazonaws.com/thetrimappbucket/'
    S3_ACCESS_KEY_ID = 'AKIAZDKFKYGLWFFFCJU3'
    S3_SECRET_KEY = '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'

class DevelopmentConfig(Config):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = True 
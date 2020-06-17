import os.path as path

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    BASE_DIR = path.abspath(path.dirname(__file__))
    BUNDLE_ERRORS = True
    DB_USER = 'postgres'
    DB_PASSWORD = 'Arsenalfc'
    DB_PORT = 'localhost:5432'
    DB_NAME = 'trim'
    SECRET_KEY = 'mYYP2dJBNeyclufoYuEJ'
    CLIENT_URL = 'http://localhost:4200'
    MAIL_BASE_URL = "https://api.mailgun.net/v3/sandboxb3e06f45528541edbc677fe253ca0c00.mailgun.org/messages"
    MAIL_API_KEY = "key-618e6125c452b712ee91e57f028fbd0f"
    MAIL_FROM = "Trim"
    MAIL_FROM_URL = "<admin@trimm.in>"
    PER_PAGE = 10

class DevelopmentConfig(Config):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = True 
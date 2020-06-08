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
    PER_PAGE = 10

class DevelopmentConfig(Config):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = True 
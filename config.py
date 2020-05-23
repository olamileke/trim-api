import os.path as path

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    BUNDLE_ERRORS = True
    DB_USER = 'postgres'
    DB_PASSWORD = 'Arsenalfc'
    DB_PORT = 'localhost:5432'
    DB_NAME = 'trim'


class DevelopmentConfig(Config):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = True 
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
    SECRET_KEY = 'x86\x1c\xcd\xa3$@\xc0\xc3x13R7(\xed/K\xb8G)x90+nNW\x0f'


class DevelopmentConfig(Config):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = True 
import os

class Config:
    SECRET_KEY = 'your-secret-key-here'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'password'
    MYSQL_DB = 'campus_connect'
    MYSQL_CURSORCLASS = 'DictCursor'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    MYSQL_DB = 'campus_connect_test'
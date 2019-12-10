#coding=utf-8
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'embedwaywx')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + \
                                             os.path.join(basedir, \
                                                          'data.sqlite'))

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

class TestConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = ('sqlite:///:memory:')
    TESTING = True

config = {
    'default': DevelopmentConfig,
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'test': TestConfig
}

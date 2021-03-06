import os
basedir = os.path.abspath(os.path.dirname(__file__))
url = 'postgresql://postgres:jefferey12@localhost/flasky'
dev_url = 'postgresql://postgres:jefferey12@localhost/flasky-dev'
test_url = 'sqlite:///'

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or ' a very hard to guess string'
  MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
  MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
  MAIL_USE_TSL = os.environ.get('MAIL_USE_TSL', 'true').lower() in ['true', 'on', '1']
  MAIL_SUPPRESS_SEND = os.environ.get(' MAIL_SUPPRESS_SEND') or False
  FLASKY_MAIL_SENDER = os.environ.get('FLASKY_MAIL_SENDER')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
  FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
  FLASKY_MAIL_SUBJECT_PREFIX = os.environ.get('MAIL_SUBJECT_PREFIX') or '<flasky>'
  FLASKY_POSTS_PER_PAGE =  os.environ.get('FLASKY_POSTS_PER_PAGE') or 10
  SQLALCHEMY_TRACK_MODIFICATIONS = False

  @staticmethod
  def init_app(app):
    pass

class DevelopmentConfig(Config):
  DEBUG = True
  TESTING = False
  SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_URL') or dev_url

class TestConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_URL') or test_url

class ProductionConfig(Config):
  SQLALCHEMY_DATABASE_URI = os.environ.get('URL') or url

config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
  }



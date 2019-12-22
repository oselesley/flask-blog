from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
login = LoginManager()

def create_app(config_name):
  if not config_name in config:
    config_name = 'default'
    
  app = Flask(__name__)
  app.config.from_object(config[config_name])
  config[config_name].init_app(app)
  from .main import main as main_blueprint
  from .auth import auth as auth_blueprint
  app.register_blueprint(main_blueprint)
  app.register_blueprint(auth_blueprint, url_prefix='/auth')

  bootstrap.init_app(app)
  db.init_app(app)
  mail.init_app(app)
  login.init_app(app)

  return app

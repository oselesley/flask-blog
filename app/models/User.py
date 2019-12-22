from .. import db
from .. import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
  __tablename__= 'users'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(64), unique=True, index=True)
  email = db.Column(db.String(64), unique=True, index=True)
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
  __password_hash = db.Column(db.String(128))

  def __repr__(self):
    return '<User {}>'.format(self.name)

  @property
  def password(self):
    raise LookupError('password is not a readable attribute!')
  
  @password.setter
  def password(self, password):
    self.__password_hash = generate_password_hash(password)
  
  def verify_password(self, password):
    return check_password_hash(self.__password_hash, password)

  @login_manager.user_loader
  def load_user(id):
    return User.query.get(int(id))


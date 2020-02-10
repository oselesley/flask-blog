from datetime import datetime
from .. import db
from .Role import Role, Permission
from .Follow import Follow
from .Post import Post
from flask import current_app, request, url_for
from .. import login_manager
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib

class User(UserMixin, db.Model):
  __tablename__= 'users'
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(64), unique=True, index=True)
  username = db.Column(db.String(64))
  email = db.Column(db.String(64), unique=True, index=True)
  location =  db.Column(db.String(64))
  about_me = db.Column(db.Text())
  member_since = db.Column(db.DateTime(), default=datetime.utcnow)
  last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
  __password_hash = db.Column(db.String(128))
  confirmed = db.Column(db.Boolean, default=False)
  avatar_hash = db.Column(db.String(256))
  posts = db.relationship('Post', backref='author', lazy='dynamic')
  followed = db.relationship('Follow', foreign_keys=[Follow.follower_id], backref=db.backref('follower', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
  follower = db.relationship('Follow', foreign_keys=[Follow.followed_id], backref=db.backref('followed', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
  comments = db.relationship('Comment', backref='author', lazy='dynamic')



# Initialization
  def __init__(self, **kwargs):
    super(User, self).__init__(**kwargs)
    self.follow(self)
    if self.role is None:
      if self.email == current_app.config['FLASKY_ADMIN']:
        self.role = Role.query.filter_by(name='Administrator').first()
      if self.role is None:
        self.role = Role.query.filter_by(default=True).first()
    if self.email and not self.avatar_hash:
      self.avatar_hash =  self.gravatar_hash()


# handles issues when email is changed including regenerating and setting a new gravatar hash 
  def change_email(self, token):
    # Not implemented yet
    # but the implementation overview involves validating the token before changing the email

    if self.validate_confirmation_token(token, email):
      self.email = email
      self.avatar_hash = self.gravatar_hash()
      db.session.add(self)


# Generate gravatar_hash
  def gravatar_hash(self):
    return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()
    

  @staticmethod
  def add_self_follows():
    for user in User.query.all():
      if not user.is_following(user):
        user.follow(user)
        db.session.add(user)
        db.session.commit()

# Generate User Avatar
  def gravatar(self, size=100, default='identicon', rating='g'):
    if request.is_secure:
      url = 'https://secure.gravatar.com/avatar'
    else:
      url = 'http://gravatar.com/avatar'
    hash = self.avatar_hash or self.gravatar_hash
    return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, default=default, size=size, rating=rating)

# Edit Last seen to current time
  def ping(self):
    self.last_seen = datetime.utcnow()
    db.session.add(self)
    db.session.commit()

  def __repr__(self):
    return '<User {}>'.format(self.name)

# Password Handler
  @property
  def password(self):
    raise LookupError('password is not a readable attribute!')

  @password.setter
  def password(self, password):
    self.__password_hash = generate_password_hash(password)
  
  def verify_password(self, password):
    return check_password_hash(self.__password_hash, password)

# Flask Login Helper function
  @login_manager.user_loader
  def load_user(id):
    return User.query.get(int(id))

# Confirmation token generation and verification
  def generate_confirmation_token(self, expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'confirm': self.id}).decode('utf-8')

  def validate_confirmation_token(self, token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
      token_obj = s.loads(token.encode('utf-8'))
    except:
      print('couldn\'t generate token')
      return False
    if token_obj['confirm'] != self.id:
      return False
    self.confirmed = True
    db.session.add(self)
    db.session.commit()
    return True
  # User Object to Json
  def to_json(self):
    return {
      'url': url_for('api.get_user', id=self.id),
      'name': self.name,
      'username': self.username,
      'posts_url': url_for('api.get_user_posts', id=self.id ),
      # 'followed_posts_url': url_for('api.get_followed_posts_url', id=self.id),
      'posts_count': self.posts.count(),
      'about_me': self.about_me,
      'member-since': self.member_since,
      'last_seen': self.last_seen

    }

  # Authentication Tokens for requests and responses
  def generate_auth_token(self, expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({ 'id': self.id }).decode('utf-8')

  @staticmethod
  def validate_auth_token(token):
    s =  Serializer(current_app.config['SECRET_KEY'])
    try:
      token_obj = s.loads(token)
    except:
      return None
    print(token_obj)
    return User.query.get_or_404(token_obj['id'])

# Permissions
  def can(self, perm):
    return self.role is not None and self.role.has_permissions(perm)

  def is_admin(self):
    return self.can(Permission.ADMIN)


# Follow
  def follow(self, user):
    if not self.is_following(user):
      f = Follow(follower=self, followed=user)
      db.session.add(f)

  def unfollow(self, user):
    f = self.followed.filter_by(followed_id=user.id).first()
    if f:
      db.session.delete(f)

  def is_following(self, user):
    if not user.id:
      return False
    return self.followed.filter_by(followed_id=user.id).first() is not None

  def is_followed_by(self, user):
    if not user.id:
      return False
    return self.follower.filter_by(follower_id=user.id).first() is not None

  @property
  def followed_posts(self):
    return Post.query.join(Follow, Follow.followed_id == Post.author_id).filter(Follow.follower_id == self.id)
    

class AnonymousUser(AnonymousUserMixin):
  def can(self, perm):
    return False

  def is_admin(self):
    return False


login_manager.anonymous_user = AnonymousUser
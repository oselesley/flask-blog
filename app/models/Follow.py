from .. import db
from datetime import datetime

class Follow(db.Model):
  __tablename__ = 'follows'
  follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
  followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
  date = db.Column(db.DateTime(), default=datetime.utcnow)
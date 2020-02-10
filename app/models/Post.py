from .. import db
from datetime import datetime
import bleach
from markdown import markdown
from flask import url_for
from app.exceptions import ValidationError

class Post(db.Model):
  __tablename__ ='posts'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(64))
  body = db.Column(db.Text())
  timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
  last_edited = db.Column(db.DateTime(), default=datetime.utcnow)
  author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  body_html = db.Column(db.Text())
  edited = db.Column(db.Boolean())
  comments = db.relationship('Comment', backref='post', lazy='dynamic')

  def __init__(self, *args, **kwargs):
    super(Post, self).__init__(*args, **kwargs)


  def ping(self):
    self.last_edited = datetime.utcnow()
    self.edited = True
    db.session.add(self)
    db.session.commit()

  @staticmethod
  def on_changed_body(target, value, old_value, initiator):
    allowed_tags = ['em', 'strong', 'pre', 'ul', 'h1', 'h2', 'h3', 'a', 'abbr', 'b', 'acronym', 'blockquote',
    'code', 'i', 'li', 'ol', 'p']
    target.body_html  = bleach.linkify(bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True))

  def to_json(self):
    return {
      'url': url_for('api.get_post', id=self.id),
      'body': self.body,
      'body_html': self.body_html,
      'author_url': url_for('api.get_author', id=self.author_id),
      'comments_url': url_for('api.get_comments', id=self.id),
      'last_edited': self.last_edited,
      'timestamp': self.timestamp,
      'comments_count': self.comments.count()
    }

  @staticmethod
  def from_json(json_post):
    body = json_post.get('body')
    title = json_post.get('title')
    if not title:
      raise ValidationError('post does no have a title!')
    if not body or body == '': 
      raise ValidationError('post does not have a body!')
    return Post(title=title, body=body)
    
db.event.listen(Post.body, 'set', Post.on_changed_body)
from flask import url_for
from .. import db
from datetime import datetime
from markdown import markdown
import bleach


class Comment(db.Model):
  __tablename__ = 'comments'
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.Text)
  body_html = db.Column(db.Text)
  timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
  last_edited = db.Column(db.DateTime(), default=datetime.utcnow)
  author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
  upvote = db.Column(db.Integer, default=0)
  downvote = db.Column(db.Integer, default=0)
  disabled = db.Column(db.Boolean, default=False)
  edited = db.Column(db.Boolean)
  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

  def ping(self):
    self.last_edited = datetime.utcnow()
    self.edited = True
    db.session.add(self)
    db.session.commit()

  @staticmethod
  def on_changed_body(target, value, old_value, initiator):
    allowed_tags = ['em', 'strong', 'pre', 'ul', 'h1', 'h2', 'h3', 'a', 'abbr', 'b', 'acronym', 'blockquote',
    'code', 'i', 'li', 'ol', 'p']
    target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True))

  def to_json(self):
    return {
      'body': self.body,
      'timestamp': self.timestamp,
      'author_url': url_for('api.get_author', id=self.author_id),
      'upvote': self.upvote,
      'downvote': self.downvote,
      'last_edited': self.last_edited,
      'url': url_for('api.get_comment', id=self.id)
    }

db.event.listen(Comment.body, 'set', Comment.on_changed_body)
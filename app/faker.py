from . import db
from faker import Faker
from .models.User import User
from .models.Role import Role
from .models.Post import Post
from  sqlalchemy.exc import IntegrityError
from random import randint

def create_users(count=100):
  fake = Faker()
  for i in range(count):
    u = User(name= fake.name(), 
      username=fake.user_name(),
      confirmed=True,
      email=fake.email(),
      location=fake.city(),
      about_me=fake.text(),
      member_since=fake.past_date(),
      password='fakepassword',
      last_seen=fake.past_date()
    )
    db.session.add(u)
    try: 
      db.session.commit()
    except IntegrityError:
      db.session.rollback()

def create_posts(count=100):
  fake=Faker()
  user_count = User.query.count()
  for i in range(count):
    u = User.query.offset(randint(0, user_count -1)).first()
    post = Post(title=fake.sentence()[:randint(12, 15)], body=fake.text(), timestamp=fake.past_date(), author=u)
    db.session.add(post)
  db.session.commit()
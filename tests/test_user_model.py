import unittest
from app.models.User import User
from flask import current_app
from app import db, create_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class UserModelTests(unittest.TestCase):
  def test_password_setter(self):
    u = User(name='ose', password = 'cat')
    self.assertIsNotNone(u._User__password_hash)

  def test_password_verification(self):
    u = User(name='ose', password = 'cat')
    self.assertTrue(u.verify_password('cat'))
    self.assertFalse(u.verify_password('dog'))

  def test_password_salts_are_random(self):
    u = User(name='ose', password = 'cat')
    u2 = User(name='damian', password = 'cat')
    self.assertTrue(u._User__password_hash != u2._User__password_hash)

  def test_generate_confirmation_token(self):
    u = User(name='ose', password = 'cat', email='ose@gmail.com', id=1)
    self.assertTrue(u.generate_confirmation_token())
    self.assertTrue(type(u.generate_confirmation_token()) == str)

  def test_verify_confirmation_token(self):
    u = User(name='ose', password = 'cat', email='ose@gmail.com', id=2)
    u2 = User(name='john', password = 'cat', email='john@gmail.com', id=5)
    token = u.generate_confirmation_token()
    token2 = u2.generate_confirmation_token()
    obj = u.validate_confirmation_token(token)
    obj2 = u.validate_confirmation_token(token2)
    print(obj)
    self.assertTrue(obj)
    # self.assertTrue(obj['confirm'] == u.id)
    # self.assertFalse(obj['confirm'] != u.id)
    
import unittest
from app.models.User import User, AnonymousUser
from flask import current_app
from app import db, create_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.models.Role import Permission, Role
from tests import BasicsTestCase



class UserModelTests(BasicsTestCase):
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
    u = User(name='ose', password = 'cat', email='ose@gmail.com')
    self.assertTrue(u.generate_confirmation_token())
    self.assertTrue(type(u.generate_confirmation_token()) == str)

  def test_verify_confirmation_token(self):
    u = User(name='ose', password = 'cat', email='ose@gmail.com')
    u2 = User(name='john', password = 'cat', email='john@gmail.com')
    token = u.generate_confirmation_token()
    token2 = u2.generate_confirmation_token()
    obj = u.validate_confirmation_token(token)
    obj2 = u.validate_confirmation_token(token2)
    self.assertTrue(obj)
    # self.assertTrue(obj['confirm'] == u.id)
    # self.assertFalse(obj['confirm'] != u.id)

  def test_user_role(self):
    Role.insert_roles()
    u = User(name='ose', password = 'cat', email='ose@gmail.com')
    self.assertTrue(u.can(Permission.COMMENT))
    self.assertTrue(u.can(Permission.WRITE))
    self.assertTrue(u.can(Permission.FOLLOW))
    self.assertFalse(u.can(Permission.ADMIN))
    self.assertFalse(u.can(Permission.MODERATE))

  def test_anonymous_user(self):
    Role.insert_roles()
    u = AnonymousUser()
    self.assertFalse(u.can(Permission.COMMENT))
    self.assertFalse(u.can(Permission.WRITE))
    self.assertFalse(u.can(Permission.FOLLOW))
    self.assertFalse(u.can(Permission.ADMIN))
    self.assertFalse(u.can(Permission.MODERATE))

  def test_admin(self):
    Role.insert_roles()
    u = User(name='ose', password = 'cat', email='leslieokoduwa@gmail.com', id=1)
    self.assertTrue(u.can(Permission.COMMENT))
    self.assertTrue(u.can(Permission.WRITE))
    self.assertTrue(u.can(Permission.FOLLOW))
    self.assertTrue(u.can(Permission.ADMIN))
    self.assertTrue(u.can(Permission.MODERATE))
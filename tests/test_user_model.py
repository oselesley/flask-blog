import unittest
from app.models.User import User


class UserModelTests(unittest.TestCase):
  def test_password_setter(self):
    u = User(name='ose', password = 'cat')
    self.assertIsNotNone(u.password)

  def test_password_verification(self):
    u = User(name='ose', password = 'cat')
    self.assertTrue(u.verify_password('cat'))
    self.assertFalse(u.verify_password('dog'))

  def test_password_salts_are_random(self):
    u = User(name='ose', password = 'cat')
    u2 = User(name='damian', password = 'cat')
    self.assertTrue(u.password != u2.password)
import os
from app import create_app, db
from app.models.Role import Role
from app.models.User import User
from app.models.Post import Post
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
  return dict(db=db, User=User, Role=Role, Post=Post)

@app.cli.command()
def test():
  import unittest
  tests = unittest.TestLoader().discover('tests')
  unittest.TextTestRunner(verbosity=2).run(tests)


# @app.cli.command()
# def test():
#   """Run the unit tests."""
#   import unittest
#   tests = unittest.TestLoader().discover('tests')
#   unittest.TextTestRunner(verbosity=2).run(tests)

# TODO
# TEST EMAIL!!!!

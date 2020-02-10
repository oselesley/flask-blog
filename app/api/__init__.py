from flask.blueprints import Blueprint

api = Blueprint('api', __name__)

from . import auth, posts, users, errors
from flask_httpauth import HTTPBasicAuth
from flask import g, jsonify, request
from ..models.User import User
from .. import db
from . import api
from .errors import forbidden, unauthorized

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email_or_token, password):
    email_or_token = request.headers.get('Authorization').split(' ')[1]
    if not email_or_token:
        email_or_token = request.json.get('email', '')
        password = request.json.get('password', '')
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = User.validate_auth_token(email_or_token)
        print(g.current_user)

        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return (user.verify_password(password))

@auth.error_handler
def auth_error():
    return  unauthorized('Invalid credentials')

@api.before_request
@auth.login_required
def before_request():
    print(g.current_user)
    if g.current_user.is_anonymous or not g.current_user.confirmed:
        return forbidden('Unconfirmed account!')

@api.route('/tokens/', methods=['GET', 'POST'])
def tokens():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials!')
    return jsonify({ 'token': g.current_user.generate_auth_token(expiration=36000), 'expiration': 3600 })
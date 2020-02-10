from . import api
from flask import request, jsonify, render_template
from ..exceptions import ValidationError



def forbidden(message):
  response = jsonify({ 'error': 'forbidden', 'message': message })
  response.status_code = 403
  return response

def unauthorized(message):
  response = jsonify({ 'error': 'unauthorized', 'message': message })
  response.status_code = 401
  return response

def bad_request(message):
  response = jsonify({ 'error': 'unauthorized', 'message': message })
  response.status_code = 404
  return response

@api.app_errorhandler(404)
def page_not_found(e):
  if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
    response = jsonify({ 'error': 'page not found' })
    response.status_code = 404
    return response
  return render_template('404.html'), 404

@api.app_errorhandler(ValidationError)
def validation_error(e):
  return bad_request(e.args[0])



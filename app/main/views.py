from flask import Flask, request, make_response, render_template, redirect, url_for, session, flash
from . import main
from .forms import NameForm
from ..models.Role import Role
from ..models.User import User
from .. import db
from flask_login import login_required
from datetime import datetime

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
  name = None
  form = NameForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    old_name = session.get('name')

    if old_name != None  and old_name != form.name.data:
      flash('Looks like you\'ve changed your name')
    print(user)
    if not user:
      session['known'] = False
      # send_mail(form.email.data, 'New User', 'mail/new_user', user=user)
    else:
      session['known'] = True

    session['name'] = form.name.data
    form.name.data = ''
    form.email.data = ''

    redirect(url_for('.index'))
  return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False), current_time=datetime.utcnow())

@main.route('/users/<name>')
def users(name):
  print(name)
  print(request.headers)
  return render_template('user.html', name=name)

@main.route('/users/pk/<int:id>')
def user_id(id):
  if id > 6:
    response = make_response('<h1>Bad Request</h1>')
    response.status_code = 400
    return response
  response = make_response('<h1>your id is {0}</h1>'.format(id))
  return response
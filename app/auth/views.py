from flask import redirect, url_for, render_template, flash, request
from . import auth
from .. import db
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm, SignupForm
from ..models.User import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()

    if user or user.verify_password(form.password.data):
      login_user(user, form.rememberme.data)
      next = request.args.get('next')
      if not next or not next.startswith('/'):
        next = url_for('main.index')
      return redirect(next)
    else:
      flash('Invalid username or password!')

  return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
  logout_user()
  flash('you have been logged out')
  return redirect(url_for('main.index'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  if form.validate_on_submit():
    user = User(name=form.name.data, email=form.email.data, password=form.password.data)
    db.session.add(user)
    db.session.commit()
    login_user(user=user)
    next = request.args.get('next')
    if not next or not next.startswith('/'):
      next = url_for('main.index')
    return redirect(next)

  return render_template('auth/signup.html', form=form)


from flask import redirect, url_for, render_template, flash, request
from . import auth
from .. import db
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm, SignupForm
from ..models.User import User
from ..mail.mail import send_mail

@auth.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()

    if not user: 
     pass
    else: 
      if user.verify_password(form.password.data):
        login_user(user, form.rememberme.data)
        next = request.args.get('next')
        if not next or not next.startswith('/'):
          next = url_for('main.index')
        return redirect(next)
    
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
    token = user.generate_confirmation_token()
    send_mail(user.email, 'Confirm your account', 'auth/mail/confirm', user=user, token=token)
    print('sent')
    flash('A confirmation email has been sent to your account')
    return redirect(url_for('auth.login'))

  return render_template('auth/signup.html', form=form)


@auth.route('/confirm/<token>')
def confirm(token):
  print(token)
  if current_user.confirmed:
    return redirect(url_for('main.index'))
  if current_user.validate_confirmation_token(token):
    flash('Hello {}!, your account has been confirmed!'.format(current_user.name))
    return redirect(url_for('main.index'))
  else:
    flash('The token is either invalid or has expired')
    return redirect(url_for('auth.login'))


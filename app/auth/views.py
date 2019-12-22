from flask import redirect, url_for, render_template, flash
from . import auth
from .forms import LoginForm
from ..models.User import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    print(user)
    if not user or not user.verify_password(form.password.data):
      flash('cannot login!')
      return render_template('login.html', form=form)
    else:
      return redirect(url_for('main.index'))
  return render_template('auth/login.html', form=form)


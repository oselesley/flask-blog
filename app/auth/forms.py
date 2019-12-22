from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators

class LoginForm(FlaskForm):
  email = StringField(label='Email', validators=[validators.DataRequired(), validators.Email()])
  password = PasswordField(label='Password', validators=[validators.DataRequired()])
  rememberme = BooleanField(label='keep me logged in')
  submit = SubmitField(label='login')

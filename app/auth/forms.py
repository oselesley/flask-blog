from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, validators, ValidationError
from ..models.User import User

class LoginForm(FlaskForm):
  email = StringField(label='Email', validators=[validators.DataRequired(), validators.Email()])
  password = PasswordField(label='Password', validators=[validators.DataRequired()])
  rememberme = BooleanField(label='keep me logged in')
  submit = SubmitField(label='login')

class SignupForm(FlaskForm):
  name = StringField(label='Fullname', validators=[validators.DataRequired(), validators.Length(1, 128)])
  username = StringField('Username', validators=[validators.DataRequired(), validators.Length(2)])
  email = StringField(label='Email', validators=[validators.DataRequired(), validators.Email(message='Enter a valid email address')])
  password = PasswordField(label='Password', validators=[validators.DataRequired(), validators.Length(min=8), validators.NoneOf(['password', '12345678'], message='invalid password!')])
  password2 = PasswordField(label='Confirm Password', validators=[validators.DataRequired(), validators.EqualTo('password')])
  submit = SubmitField('Register')

  def validate_email(self, field):
    if User.query.filter_by(email=field.data).first():
      raise ValidationError('Email already registered!')

  # def validate_name(self, field):
  #   if User.query.filter_by(name=field.name).first():
  #     raise ValidationError('Username in use!')
  
  def validate_username(self, field):
    if User.query.filter_by(username=field.data).first() is not None:
      raise ValidationError('This username already exists!')
  

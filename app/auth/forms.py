from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators

class LoginForm(FlaskForm):
  email = StringField(label='Email', validators=[validators.DataRequired(), validators.Email()])
  password = PasswordField(label='Password', validators=[validators.DataRequired()])
  submit = SubmitField(label='login')

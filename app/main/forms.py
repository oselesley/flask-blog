from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
import wtforms.validators as validate
from wtforms.validators import DataRequired



class NameForm(FlaskForm):
  name = StringField('Your Name', validators=[DataRequired()])
  email = StringField('Your Email', validators=[DataRequired(), validate.Email('Enter a valid email address')])
  password = PasswordField('Your Password', validators=[validate.Length(min=1), validate.NoneOf(['password'])])
  password2 = PasswordField('Confirm Password', validators=[validate.EqualTo('password')])
  submit = SubmitField('Submit')

from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, BooleanField, SelectField
import wtforms.validators as validate
from wtforms.validators import DataRequired, Regexp, ValidationError
from ..models.Role import Role
from ..models.User import User



class NameForm(FlaskForm):
  name = StringField('Your Name', validators=[DataRequired()])
  email = StringField('Your Email', validators=[DataRequired(), validate.Email('Enter a valid email address')])
  password = PasswordField('Your Password', validators=[validate.Length(min=1), validate.NoneOf(['password'])])
  password2 = PasswordField('Confirm Password', validators=[validate.EqualTo('password')])
  submit = SubmitField('Submit')



class EditProfileForm(FlaskForm):
  name = StringField('Fullname', validators=[DataRequired(), validate.Length(0, 128)])
  username = StringField('Username', validators=[DataRequired(), validate.Length(0, 64)])
  location = StringField('Location', validators=[validate.Length(0, 128)])
  about_me = TextAreaField('About me')
  submit = SubmitField('Update Profile')

class EditProfileAdminForm(FlaskForm):
  name = StringField('Fullname', validators=[DataRequired(), validate.Length(0, 128)])
  username = StringField('Fullname', validators=[DataRequired(), validate.Length(0, 128), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters numbers, dots or underscores') ])
  email = StringField('Email', validators=[DataRequired(), validate.Length(0, 64), validate.Email()])
  location = StringField('Location', validators=[DataRequired(), validate.Length(0, 128)])
  confirmed = BooleanField('confirmed')
  role = SelectField('Role', coerce=int)
  about_me = TextAreaField('About Me')
  submit = SubmitField('Update Profile')

  def __init__(self, user, *args, **kwargs):
    super(EditProfileAdminForm, self).__init__(*args, **kwargs)
    self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
    self.user = user

  def validate_email(self, field):
    if field.data != self.user.email and User.query.filter_by(field.data).first():
      raise ValidationError('Email already registered!')

  def validate_username(self, field):
    if field.data != self.user.username and User.query.filter_by(field.data).first():
      raise ValidationError('Username already in use!')

class PostForm(FlaskForm):
  title = StringField(label='Title', validators=[DataRequired(), validate.Length(0, 50)])
  body = PageDownField(label= 'What\'s On your mind...?')
  submit = SubmitField(label='Submit')

class CommentForm(FlaskForm):
  body = PageDownField('Enter your comments', validators=[DataRequired()])
  submit = SubmitField('submit')

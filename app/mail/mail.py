from flask_mail import Message
from flask_mail_sendgrid import MailSendGrid
from .. import create_app
from flask import render_template
from threading import Thread
# from flask import current_app
import os

app = create_app('default')
mail = MailSendGrid(app)

def send_async_email(app, msg):
  with app.app_context():
    mail.send(msg)

def send_mail(to, subject, template, **kwargs):
  msg = Message(app.config.get('FLASKY_MAIL_SUBJECT_PREFIX') + subject, sender=app.config.get('FLASKY_MAIL_SENDER'), recipients=[to])
  msg.html = render_template('{}.html'.format(template), **kwargs)
  msg.body = render_template('{}.txt'.format(template), **kwargs)
  # mail.send(msg)
  thr = Thread(target=send_async_email, args=[app, msg])
  thr.start()
  return thr
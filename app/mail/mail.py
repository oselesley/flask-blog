from flask_mail import Mail, Message
from flask import render_template
from threading import Thread
from app import app
import os

mail = Mail(app)

def send_async_email(app, msg):
  with app.app_context():
    mail.send(msg)

def send_mail(to, subject, template, **kwargs):
  msg = Message(os.environ.get('MAIL_SUBJECT_PREFIX') + subject, sender=os.environ.get('MAIL_USERNAME'), recipients=[to])
  msg.html = render_template('{}.html'.format(template), **kwargs)
  msg.body = render_template('{}.txt'.format(template), **kwargs)
  thr = Thread(target=send_async_email, args=[app, msg])
  thr.start()
  return thr
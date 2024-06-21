from flask_mail import Message
from app import app
from models import mail

with app.app_context():
    message = Message(subject='test', recipients=['2562136308@qq.com'], body='test')
    mail.send(message)
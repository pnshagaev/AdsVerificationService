from flask_mail import Message

from flask_mail import Mail
from application.config import DefaultConfig


def send_mail(recipients, file_path):
    msg = Message(
        'good night',
        sender=DefaultConfig.MAIL_DEFAULT_SENDER,
        recipients=recipients)
    msg.body = "your file"
    print(file_path)
    with open(file_path, 'rb') as fp:
        msg.attach(file_path, "application/zip", fp.read())
    try:
        from application.app import app
        with app.app_context():
            mail = Mail(app)
            mail.send(msg)
    except Exception as e:
        print(e)

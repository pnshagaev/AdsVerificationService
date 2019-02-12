from datetime import datetime

from flask_mail import Mail
from flask_mail import Message

from application.config import DefaultConfig


def send_mail(recipients, file_path, chunk_number, total_chunks):
    msg = Message(f'AdsScreenshot {datetime.now()} yandex ({chunk_number}/{total_chunks})',
                  sender=DefaultConfig.MAIL_DEFAULT_SENDER,
                  recipients=recipients,
                  body="Скриншоты по вашим запросам во вложении. Это автоматическая рассылка, не отвечайте на письмо. При возникновении вопросов обращайтесь к вашему менеджеру.")

    with open(file_path, 'rb') as fp:
        msg.attach(file_path, "application/zip", fp.read())
    try:
        from application.app import app
        with app.app_context():
            mail = Mail(app)
            mail.send(msg)
    except Exception as e:
        print(e)

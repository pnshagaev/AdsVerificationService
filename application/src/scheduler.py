from apscheduler.schedulers.background import BackgroundScheduler
from application.src.screenshot import search_words
from datetime import datetime
from application.src.mail import send_mail

scheduler = BackgroundScheduler()
scheduler.start()


def process_words(email, words):
    words_path = search_words(words)
    send_mail([email], words_path)


def add_scheduled_job(email, words):
    scheduler.add_job(func=process_words, args=(email, words), trigger="date", next_run_time=datetime.now())


from apscheduler.schedulers.background import BackgroundScheduler
from application.src.screenshot import search_words, delete_archive
from datetime import datetime
from application.src.mail import send_mail

scheduler = BackgroundScheduler()
scheduler.start()


def process_words(email, words):
    word_chunks = [words[x:x + 20] for x in range(0, len(words), 20)]
    total_chunks = len(word_chunks)
    for i, chunk in enumerate(word_chunks):
        name = 'yandex_' + str(datetime.now())
        try:
            words_path = search_words(chunk, name)
            send_mail([email], words_path, i+1, total_chunks)
        except Exception as e:
            print(e)
        delete_archive('./' + name + '.zip')


def add_scheduled_job(email, words):
    scheduler.add_job(func=process_words, args=(email, words), trigger="date", next_run_time=datetime.now())

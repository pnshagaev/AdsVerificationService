from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import shutil
import os


def setup_driver():
    driver_name = '/Users/pavel/bin/chromedriver'
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1000,1500")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(driver_name, chrome_options=chrome_options)
    return driver


def save_yandex_screenshot(driver, word, path_to_save):
    driver.get(f'https://yandex.ru/search/?text={word}')
    driver.save_screenshot('{}/{}.png'.format(path_to_save, str(word)))


def create_folder(path):
    folder_to_save = Path(path)
    folder_to_save.mkdir(exist_ok=True)


def search_words(words, name):
    path = './' + name
    create_folder(path)
    driver = setup_driver()
    try:
        for word in words:
            save_yandex_screenshot(driver, word.rstrip(), path)
    except FileNotFoundError:
        print(f'incorrect file path: {words_file}')
    shutil.make_archive(name, 'zip', path)
    driver.quit()
    return path + '.zip'


def delete_archive(path):
    os.remove(path)

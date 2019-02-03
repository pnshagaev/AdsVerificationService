import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def setup_driver():
    driver_name = 'chromedriver'
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1000,1500")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(driver_name, chrome_options=chrome_options)
    return driver


def save_yandex_screenshot(driver, word, path_to_save):
    driver.get(f'https://yandex.ru/search/?text={word}')
    driver.save_screenshot('yandex_{}/{}.png'.format(path_to_save, str(word)))


def create_folder(path):
    folder_to_save = Path(path)
    folder_to_save.mkdir(exist_ok=True)


def search_words(words):
    path = './' + str(datetime.datetime.now())
    create_folder(path)
    driver = setup_driver()
    try:
        for word in words:
            save_yandex_screenshot(driver, word.rstrip(), path)
            print(f'done: {word}')
    except FileNotFoundError:
        print(f'incorrect file path: {words_file}')
    driver.quit()
    return path

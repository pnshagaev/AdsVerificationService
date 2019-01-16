import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import argparse

def setup_driver():
    driver_name = 'chromedriver'
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1000,1500")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(driver_name, chrome_options=chrome_options)
    return driver


def save_screenshot(driver, word, path_to_save):
    driver.get(f'https://yandex.ru/search/?text={word}')
    driver.save_screenshot('{}/{}.png'.format(path_to_save, str(word)))


def create_folder(path):
    folder_to_save = Path(path)
    folder_to_save.mkdir(exist_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='words_file', help='path of file with search words', required=True)
    args = parser.parse_args()
    path = './' + str(datetime.datetime.now())
    driver = setup_driver()
    words_file = args.words_file
    try:
        with open(words_file) as file:
            create_folder(path)
            for line in file:
                line = line.rstrip()
                save_screenshot(driver, line.rstrip(), path)
                print(f'done: {line}')
    except FileNotFoundError:
        print(f'incorrect file path: {words_file}')
    driver.quit()


if __name__ == '__main__':
    main()

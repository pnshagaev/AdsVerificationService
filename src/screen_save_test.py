from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime

if __name__ == '__main__':
    DRIVER = 'chromedriver'
    rome_options = Options()
    rome_options.add_argument("--window-size=1000,1500")
    rome_options.add_argument("--headless")
    driver = webdriver.Chrome(DRIVER, chrome_options=rome_options)
    start = datetime.datetime.now()
    for i in range(1000):
        start_iter = datetime.datetime.now()
        driver.get(f'https://yandex.ru/search/?text=test{i}')
        screenshot = driver.save_screenshot('my_screenshot.png')
        driver.save_screenshot('/Users/pnshagaev/Desktop')
        if i % 100 == 0:
            print(i)
            print(f'time is: {datetime.datetime.now() - start_iter}')
    print(f'full_time is: {datetime.datetime.now() - start}')

    driver.quit()

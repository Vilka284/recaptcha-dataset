import time
import random
import weakref
import os
import requests
import warnings

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from download_image import path_to_driver


warnings.filterwarnings("ignore", category=DeprecationWarning)
url = 'https://www.google.com/recaptcha/api2/demo'


class Captcha:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=500,600")
        chrome_options.add_argument("--window-position=150,130")
        self.browser = webdriver.Chrome(
            executable_path=path_to_driver,
            options=chrome_options)

    def switch_to(self, type, frame_number=None):
        if type == 'default':
            self.browser.switch_to.default_content()
        elif type == 'iframe':
            iframe = self.browser.find_elements_by_tag_name('iframe')[frame_number]  # iframe 0 contains captcha border and iframe 2 contains all captcha details
            self.browser.switch_to.frame(iframe)

    def refreshing(self):
        try:
            time.sleep(3)
            act = self.browser.find_elements_by_css_selector(".button-holder.reload-button-holder")[0]
            # act = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="recaptcha-reload-button"]"]')))
            act.click()
        except Exception as ex:
            print(ex)

    def table_info(self):
        try:
            self.sleep(3)
            table_name = self.browser.find_elements_by_xpath('//table[starts-with(@class, "rc-imageselect-table")]')[0]
            value_of_squares = table_name.get_attribute('class').split('-')[-1]
            if value_of_squares == '44':
                print('It\'s table with 16 squares')
                print('Refreshing')
                self.refreshing()
                time.sleep(2)
                self.table_info()
            elif value_of_squares == '33':
                print('It\'s table with 9 squares')
            self.sleep(3)
            upper_class_name = self.browser.find_element_by_xpath("//div[starts-with(@class, 'rc-imageselect-desc')]")
            childs = upper_class_name.find_elements_by_xpath("./child::*")
            # class_name = childs[0]
            class_name = upper_class_name.find_element_by_tag_name('strong')
            self.sleep(3)
            if len(childs) >= 2:
                print('Table with dissapearing images')
                self.refreshing()
                time.sleep(2)
                self.table_info()
            return class_name.text
        except Exception as ex:
            print(ex)

    def captcha_border(self):
        try:
            act = self.browser.find_elements_by_css_selector('.recaptcha-checkbox-border')[0]
            act.click()
        except Exception as ex:
            print(ex)

    def accept_captcha(self):
        try:
            act = self.browser.find_element_by_css_selector('.rc-button-default goog-inline-block')
            act.click()
        except Exception as ex:
            print(ex)

    def quit(self):
        self.browser.close()
        self.browser.quit()

    def sleep(self, time):
        self.browser.implicitly_wait(time)

    def download_image(self):
        try:
            image_box = self.browser.find_element_by_xpath('//img[starts-with(@class, "rc-image-tile")]')
            image_path = image_box.get_attribute('src')
            img_data = requests.get(image_path).content
            with open(os.path.join(os.getcwd(), 'photos', 'original', 'payload.jpg'), 'wb') as handler:
                handler.write(img_data)
        except Exception as ex:
            print(ex)


def main():
    captcha = Captcha()
    captcha.browser.get(url)
    captcha.sleep(5)

    captcha.switch_to('iframe', 0)
    captcha.captcha_border()

    captcha.switch_to('default')
    captcha.sleep(5)

    captcha.switch_to('iframe', 2)
    captcha.sleep(3)

    category = captcha.table_info()
    captcha.sleep(2)
    with open(os.path.join(os.getcwd(), 'photos', 'category.txt'), 'w', encoding='utf-8') as handler:
        handler.write(category)

    captcha.download_image()

    captcha.quit()


if __name__ == '__main__':
    main()

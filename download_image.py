import time

import pyautogui
import os
import requests

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options


url = 'https://www.google.com/recaptcha/api2/demo'

# Replace with your driver
# Windows - chromedriver.exe v.96.4664
# Linux - chromedriver v.96.4664
path_to_driver = os.path.join(os.getcwd(), 'driver', 'chromedriver.exe')


def main():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=500,600")
    chrome_options.add_argument("--window-position=150,130")
    # chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

    browser = webdriver.Chrome(executable_path=path_to_driver, options=chrome_options)
    browser.get(url)
    browser.implicitly_wait(5)

    iframe = browser.find_elements_by_tag_name('iframe')[0]  # switching to frame that contains recaptcha
    browser.switch_to.frame(iframe)
    act = browser.find_elements_by_css_selector('.recaptcha-checkbox-border')[0]
    act.click()

    browser.switch_to.default_content()

    iframe = browser.find_elements_by_tag_name('iframe')[2]  # switching to frame that has images and text
    browser.switch_to.frame(iframe)
    image_box = browser.find_element_by_xpath('//img[starts-with(@class, "rc-image-tile")]')
    image_path = image_box.get_attribute('src')
    browser.get(image_path)

    # actionChains = ActionChains(browser)
    # actionChains.context_click().perform()

    img_data = requests.get(image_path).content
    with open(os.path.join(os.getcwd(), 'photos', 'original', 'payload.jpg'), 'wb') as handler:
        handler.write(img_data)

    # pyautogui.hotkey('ctrl', 's')
    # time.sleep(2)
    # pyautogui.press('Enter')
    # time.sleep(2)
    # browser.quit()


if __name__ == '__main__':
    main()

import time
import random
import weakref

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from colorama import init, Fore, Back, Style
from download_image import path_to_driver

# init(autoreset=True)
init(convert=True)

canon = False


def get_class_name():
    global canon
    try:
        upper_class_name = browser.find_element_by_xpath("//div[@class = 'rc-imageselect-desc-no-canonical']")  # not refreshing squares
        canon = False
        class_name = upper_class_name.find_elements_by_xpath("./child::*")[0]
        print(Back.YELLOW + class_name.text + Style.RESET_ALL)
    except NoSuchElementException:
        upper_class_name = browser.find_element_by_xpath("//div[@class = 'rc-imageselect-desc']")  # refreshing squares
        canon = True
        class_name = upper_class_name.find_elements_by_xpath("./child::*")[0]
        print(Back.YELLOW + class_name.text + Style.RESET_ALL)
    return class_name.text


def sleep(sec=2):
    print(Back.RED + 'Sleeping for', sec, 'seconds, wait...' + Style.RESET_ALL)
    for i in range(sec):
        time.sleep(1)
        print(Back.RED + Style.BRIGHT + str(i + 1), '...' + Style.RESET_ALL)


def initiating_random_clicks():
    list_of_squares = browser.find_elements_by_css_selector('.rc-image-tile-wrapper')
    list_of_checkbox_squares = browser.find_elements_by_css_selector('.rc-image-tile-wrapper')  # if square is clicked once
    random_clicks = random.randint(1, 9)
    print(Back.CYAN + 'Initiating', random_clicks, 'random_clicks' + Style.RESET_ALL)
    for i in range(random_clicks):
        random_square = random.randint(0, 8)
        print(Back.MAGENTA + 'Clicking random square with number ' + str(random_square + 1) + Style.RESET_ALL)
        try:
            list_of_squares[random_square].click()
            sleep(2)
        except ElementClickInterceptedException:
            list_of_checkbox_squares[random_square].click()
            sleep(2)
        except StaleElementReferenceException:
            print(Back.RED + Fore.MAGENTA + "Now working now..." + Style.RESET_ALL)
            sleep(2)


url = 'https://www.google.com/recaptcha/api2/demo'
chrome_options = Options()
chrome_options.add_argument("--window-size=500,600")
chrome_options.add_argument("--window-position=150,130")
# chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])

print(Back.GREEN + 'Opening browser' + Style.RESET_ALL)

browser = webdriver.Chrome(executable_path=path_to_driver, options=chrome_options)
browser.implicitly_wait(5)
browser.get(url)
sleep(4)
iframe = browser.find_elements_by_tag_name('iframe')[0]  # switching to frame that contains recaptcha
browser.switch_to.frame(iframe)
act = browser.find_elements_by_css_selector('.recaptcha-checkbox-border')[0]
print(Back.GREEN + 'Clicking checkbox I\'m not robot ' + Style.RESET_ALL)
act.click()

# pyautogui_acts.smooth_moveTo(626, 262, 1)

browser.switch_to.default_content()

sleep(3)

iframe = browser.find_elements_by_tag_name('iframe')[2]  # switching to frame that has images and text
browser.switch_to.frame(iframe)
# refreshing
act = browser.find_elements_by_css_selector(".button-holder.reload-button-holder")[0]
act.click()

# print(browser.find_element_by_xpath('//div[@class="rc-imageselect-desc"]/div[last()]'))

table_name = browser.find_elements_by_xpath('//table[starts-with(@class, "rc-imageselect-table")]')[0]
value_of_squares = table_name.get_attribute('class').split('-')[-1]
if value_of_squares == '44':
    print(Back.YELLOW + 'It\'s table with 16 squares' + Style.RESET_ALL)
elif value_of_squares == '33':
    print(Back.YELLOW + 'It\'s table with 9 squares' + Style.RESET_ALL)

sleep(2)
print(Back.YELLOW + 'Class name :')

# file = open(file='all_classes.txt', mode='a', encoding='utf-8')
# for i in range(50):
#     act = browser.find_elements_by_css_selector(".button-holder.reload-button-holder")[0]
#     act.click()
#     sleep(2)
#     file.write(get_class_name() + "\n")
# file.close()


sleep(2)
act = browser.find_elements_by_css_selector(".button-holder.reload-button-holder")[0]
sleep(2)
print(Back.GREEN + 'Refreshing images' + Style.RESET_ALL)
act.click()
sleep(2)
initiating_random_clicks()

# act = browser.find_elements_by_css_selector('.rc-button-default goog-inline-block')[0]
# act.click()
print(Back.GREEN + 'Quiting browser' + Style.RESET_ALL)
sleep(2)
browser.quit()

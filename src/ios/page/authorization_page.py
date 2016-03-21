from time import sleep
import time
import unittest
from src.ios.data.bkstg_locators import *


class AuthorizationPage(unittest.TestCase):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def log_in(self, email, password):
        email_button = self.driver.find_element_by_name(EMAIL_BUTTON)
        email_button.click()
        print('User taps on "EMAIL" button')
        self.driver.implicitly_wait(2)
        email_field = self.driver.find_element_by_xpath(EMAIL_FIELD)
        print('User enters his address - "%s"' % email)
        email_field.send_keys(email)
        auth_next_button = self.driver.find_element_by_name(AUTH_NEXT_BUTTON)
        print('User taps "NEXT" button')
        auth_next_button.click()
        password_field = self.driver.find_element_by_xpath(PASSWORD_FIELD)
        print('User enters his password')
        password_field.send_keys(password)
        log_in_button = self.driver.find_element_by_name(LOG_IN_BUTTON)
        print('User taps "LOG IN" button')
        log_in_button.click()
        sleep(1)

    def sign_up_via_email(self):
        email_button = self.driver.find_element_by_name(EMAIL_BUTTON)
        email_button.click()
        print('User taps on "EMAIL" button')
        timestamp = str(time.time()).split('.')[0]
        email = 'aleksey%s@bkstg.com' % timestamp
        nickname = 'aleksey%s' % timestamp
        username = 'Aleksey %s' % timestamp
        email_field = self.driver.find_element_by_xpath(EMAIL_FIELD)
        print('User enters his address - "%s"' % email)
        email_field.send_keys(email)
        auth_next_button = self.driver.find_element_by_name(AUTH_NEXT_BUTTON)
        print('User taps "NEXT" button')
        auth_next_button.click()
        create_password_field = self.driver.find_element_by_xpath(CREATE_PASSWORD_FIELD)
        print('User enters his password')
        create_password_field.send_keys('qqqqqqqq')
        print('User taps "NEXT" button')
        auth_next_button.click()
        nickname_field = self.driver.find_element_by_xpath(NICKNAME_FIELD)
        print('User enters his nickname - "%s"' % nickname)
        nickname_field.send_keys(nickname)
        print('User taps "NEXT" button')
        auth_next_button.click()
        username_field = self.driver.find_element_by_xpath(USERNAME_FIELD)
        print('User enters his name')
        username_field.send_keys(username)
        sign_up_button = self.driver.find_element_by_name(SIGN_UP_BUTTON)
        print('User taps "Sign UP" button')
        sign_up_button.click()
        notify_me_button = self.driver.find_element_by_name(NOTIFY_ME_BUTTON)
        notify_me_button.click()
        sleep(1)







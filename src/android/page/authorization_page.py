__author__ = 'Roma'
from time import sleep
import time
import unittest
from src.android.data.bkstg_locators import *


class AuthorizationPage(unittest.TestCase):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def signUpWithEmail(self):
        timestamp = str(time.time()).split('.')[0]
        email = 'test%s@bkstg.com' % timestamp
        nickname = 'test%s' % timestamp
        password = 'pass%s' % timestamp
        first_last_name = 'first last'
        sign_up_email = self.driver.find_element_by_id(EMAIL_BUTTON)
        print('User tap on Email button')
        sign_up_email.click()
        email_field = self.driver.find_element_by_id(EMAIL_FIELD)
        print('User entered hid Email - "%s"' % email)
        email_field.send_keys(email)
        next_button = self.driver.find_element_by_id(NEXT_BUTTON)
        print('User tap on Next button')
        next_button.click()
        create_password_field = self.driver.find_element_by_xpath(PASSWORD_FIELD)
        print('User entered password')
        create_password_field.send_keys(password)
        next_button.click()
        nickname_field = self.driver.find_element_by_xpath(NICKNAME_FIELD)
        print('User entered nickname - "%s"' % nickname)
        nickname_field.send_keys(nickname)
        next_button.click()
        first_last_name_field = self.driver.find_element_by_xpath(FIRST_LAST_NAME_FIELD)
        print('User entered his first and last name - "%s"' % first_last_name)
        first_last_name_field.send_keys(first_last_name)
        sign_up_button = self.driver.find_element_by_id(SIGN_UP_BUTTON)
        print('User tap on Sign Up button')
        sign_up_button.click()
        cool_button = self.driver.find_element_by_id(COOL_BUTTON)
        print('User tap on Cool button')
        cool_button.click()

    def logIn(self, email, password):
        sign_up_email = self.driver.find_element_by_id(EMAIL_BUTTON)
        print('User tap on Email button')
        sign_up_email.click()
        email_field = self.driver.find_element_by_id(EMAIL_FIELD)
        print('User entered hid Email - "%s"' % email)
        email_field.send_keys(email)
        next_button = self.driver.find_element_by_id(NEXT_BUTTON)
        print('User tap on Next button')
        next_button.click()
        password_field = self.driver.find_element_by_xpath(PASSWORD_FIELD)
        print('User entered password')
        password_field.send_keys(password)
        sign_up_button = self.driver.find_element_by_id(SIGN_UP_BUTTON)
        print('User tap on Sign Up button')
        sign_up_button.click()

    def checkSignIn(self):
        print('Check if user is logged in')
        search_field = self.driver.find_elements_by_id(SEARCH_FIELD)
        if len(search_field) >= 1:
            print('User is logged in')
        else:
            self.fail('User is not logged in')
        sleep(3)

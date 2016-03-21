import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
__author__ = 'Roma'
from src.android.page.authorization_page import AuthorizationPage
from src.android.test.android_capabilities import desired_caps
import unittest
from appium import webdriver


class AuthorizationTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        driver = self.driver
        global authorization_page
        authorization_page = AuthorizationPage(driver)
        self.driver.implicitly_wait(10)

    def test_sign_up(self):
        authorization_page.signUpWithEmail()
        authorization_page.checkSignIn()

    def test_log_in(self):
        authorization_page.logIn('roma@bkstg.com', 'qa123123')
        authorization_page.checkSignIn()

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
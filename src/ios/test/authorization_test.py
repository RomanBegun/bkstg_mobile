from src.ios.page.cards_navigation_page import CardsNavigationPage
from src.ios.page.authorization_page import AuthorizationPage
from src.ios.test.ios_capabilities import desired_caps
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import unittest
from appium import webdriver


class AuthorizationTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        driver = self.driver
        global auth, navigation
        auth = AuthorizationPage(driver)
        navigation = CardsNavigationPage(driver)
        self.driver.implicitly_wait(10)

    def test_sign_in(self):
        auth.log_in('aleksey@bkstg.com', 'qqqqqqqq')
        navigation.accept_permissions()
        navigation.check_sign_in()

    def test_sign_up(self):
        auth.sign_up_via_email()
        navigation.accept_permissions()
        navigation.check_sign_in()

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

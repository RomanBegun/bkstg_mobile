import os.path
import sys
import unittest
from src.android.page.authorization_page import AuthorizationPage
from src.android.page.cards_navigation_page import CardsNavigationPage
from src.android.test.android_capabilities import desired_caps
from appium import webdriver
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
__author__ = 'Roma'


class CardsNavigationTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        driver = self.driver
        global authorization_page, cards_navigation_page
        authorization_page = AuthorizationPage(driver)
        cards_navigation_page = CardsNavigationPage(driver)
        self.driver.implicitly_wait(10)

    def test_add_hub_from_search(self):
        authorization_page.signUpWithEmail()
        cards_navigation_page.search_hub('5SOS')
        cards_navigation_page.addHub('5SOS')
        cards_navigation_page.cancelSearch()
        cards_navigation_page.check_added_hub('5SOS')
        cards_navigation_page.cancelSearch()
        cards_navigation_page.removeHub('5SOS')

    def test_add_ghost_card(self):
        authorization_page.signUpWithEmail()
        cards_navigation_page.search_hub('nopresentcard')
        cards_navigation_page.addGhostCard('nopresentcard')

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()


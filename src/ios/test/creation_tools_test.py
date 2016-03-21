from src.ios.page.card_page import CardPage
from src.ios.page.cards_navigation_page import CardsNavigationPage
from src.ios.page.authorization_page import AuthorizationPage
from src.ios.test.ios_capabilities import desired_caps
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import unittest
from appium import webdriver


class CreationToolsTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        driver = self.driver
        global auth, navigation, card
        auth = AuthorizationPage(driver)
        navigation = CardsNavigationPage(driver)
        card = CardPage(driver)
        self.driver.implicitly_wait(10)

    def test_creation_tools(self):
        hub_name = 'jackson harris'
        auth.sign_up_via_email()
        navigation.accept_permissions()
        navigation.search_hub(hub_name)
        navigation.add_hub(hub_name)
        navigation.expand_hub()
        card.open_hub_section('Community')

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()


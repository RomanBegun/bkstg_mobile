from src.ios.page.cards_navigation_page import CardsNavigationPage
import unittest
from appium import webdriver
from src.ios.page.authorization_page import AuthorizationPage
from src.ios.test.ios_capabilities import desired_caps


class CardsNavigationTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        driver = self.driver
        global auth, navigation
        auth = AuthorizationPage(driver)
        navigation = CardsNavigationPage(driver)
        self.driver.implicitly_wait(10)

    #def test_hub(self):
    #    authorization_page.signUpViaEmail()
    #    cards_navigation_page.addHub('ariana grande')
    #    cards_navigation_page.removeHub('ariana grande')

    def test_search_hub(self):
        hub_name = 'jackson harris'
        auth.sign_up_via_email()
        navigation.accept_permissions()
        navigation.search_hub(hub_name)
        navigation.add_hub(hub_name)
        navigation.remove_hub(hub_name)

    def test_add_ghost_hub(self):
        auth.sign_up_via_email()
        navigation.accept_permissions()
        navigation.add_ghost_hub('Alexey')

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

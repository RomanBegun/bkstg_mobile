import unittest
from time import sleep
from src.android.page.authorization_page import AuthorizationPage
from src.android.page.cards_navigation_page import CardsNavigationPage
from src.android.page.hub_feed_page import HubFeedPage
from src.android.test.android_capabilities import desired_caps
from src.android.page.community_page import CommunityPage
from appium import webdriver
__author__ = 'Roma'


class HubFeedTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        driver = self.driver
        global authorization_page, cards_navigation_page, hub_feed_page, community_page
        authorization_page = AuthorizationPage(driver)
        cards_navigation_page = CardsNavigationPage(driver)
        hub_feed_page = HubFeedPage(driver)
        community_page = CommunityPage(driver)
        self.driver.implicitly_wait(10)

    def test_community_comment(self):
        authorization_page.logIn('mikeshinoda@bkstg.com', 'mikeshinoda')
        authorization_page.checkSignIn()
        cards_navigation_page.expandHub('Linkin Park')
        hub_feed_page.openBkstgSubMenu()
        hub_feed_page.selectSubMenuItem('Community')
        hub_feed_page.postComment('Test comment')

    def test_like_unlike_community_post(self):
        authorization_page.logIn('mikeshinoda@bkstg.com', 'mikeshinoda')
        authorization_page.checkSignIn()
        cards_navigation_page.expandHub('Linkin Park')
        hub_feed_page.openBkstgSubMenu()
        hub_feed_page.selectSubMenuItem('Community')
        hub_feed_page.postLike()
        sleep(3)
        hub_feed_page.postUnlike()

    def test_select_community_filter(self):
        authorization_page.logIn('mikeshinoda@bkstg.com', 'mikeshinoda')
        authorization_page.checkSignIn()
        cards_navigation_page.expandHub('Linkin Park')
        hub_feed_page.openBkstgSubMenu()
        hub_feed_page.selectSubMenuItem('Community')
        community_page.selectCommunityFilter('NEW')

    def test_select_community_promoted_hashtags(self):
        authorization_page.logIn('mikeshinoda@bkstg.com', 'mikeshinoda')
        authorization_page.checkSignIn()
        cards_navigation_page.expandHub('Linkin Park')
        hub_feed_page.openBkstgSubMenu()
        hub_feed_page.selectSubMenuItem('Community')
        community_page.promotedHashtags('3')

    def test_share_community_post(self):
        authorization_page.logIn('mikeshinoda@bkstg.com', 'mikeshinoda')
        authorization_page.checkSignIn()
        cards_navigation_page.expandHub('Linkin Park')
        hub_feed_page.openBkstgSubMenu()
        hub_feed_page.selectSubMenuItem('Community')
        hub_feed_page.chooseShareMethod('SMS')

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

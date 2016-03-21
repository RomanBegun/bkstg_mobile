import os.path
import sys
import unittest
from src.android.page.authorization_page import AuthorizationPage
from src.android.page.cards_navigation_page import CardsNavigationPage
from src.android.test.android_capabilities import desired_caps
from src.android.page.creation_tools_page import CreationToolsPage
from src.android.page.hub_feed_page import HubFeedPage
from appium import webdriver
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
__author__ = 'Roma'


class CreationToolsTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        driver = self.driver
        global authorization_page, cards_navigation_page, creation_tools_page, hub_feed_page
        authorization_page = AuthorizationPage(driver)
        cards_navigation_page = CardsNavigationPage(driver)
        creation_tools_page = CreationToolsPage(driver)
        hub_feed_page = HubFeedPage(driver)
        self.driver.implicitly_wait(10)

    def test_create_text_post(self):
        authorization_page.logIn('mikeshinoda@bkstg.com', 'mikeshinoda')
        authorization_page.checkSignIn()
        cards_navigation_page.expandHub('Linkin Park')
        hub_feed_page.openCreationTools()
        creation_tools_page.addTextInView()
        creation_tools_page.clickPost()
        hub_feed_page.uploadPostMessage()

    def test_create_image_post(self):
        authorization_page.logIn('mikeshinoda@bkstg.com', 'mikeshinoda')
        authorization_page.checkSignIn()
        cards_navigation_page.expandHub('Linkin Park')
        hub_feed_page.openCreationTools()
        creation_tools_page.addLastGalleryPhoto()
        creation_tools_page.addText()
        creation_tools_page.clickPost()
        hub_feed_page.uploadPostMessage()

    def test_create_gallery_media_post(self):
        authorization_page.logIn('mikeshinoda@bkstg.com', 'mikeshinoda')
        authorization_page.checkSignIn()
        cards_navigation_page.expandHub('Linkin Park')
        hub_feed_page.openCreationTools()
        creation_tools_page.openGallery()
        creation_tools_page.chooseMediaContent('Photo')
        creation_tools_page.chooseMediaItem()
        creation_tools_page.addText()
        creation_tools_page.clickPost()
        hub_feed_page.uploadPostMessage()

    def test_create_camera_post(self):
        authorization_page.logIn('mikeshinoda@bkstg.com', 'mikeshinoda')
        authorization_page.checkSignIn()
        cards_navigation_page.expandHub('Linkin Park')
        hub_feed_page.openCreationTools()
        creation_tools_page.makePhoto()
        creation_tools_page.addText()
        creation_tools_page.clickPost()
        hub_feed_page.uploadPostMessage()

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()

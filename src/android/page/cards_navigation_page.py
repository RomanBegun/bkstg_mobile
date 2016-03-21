import os
import sys
from time import sleep
import unittest
from appium.webdriver.common.touch_action import TouchAction
from src.android.data.bkstg_locators import *
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
__author__ = 'Roma'


class CardsNavigationPage(unittest.TestCase):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def addHub(self, card_name):
        add_hub_button = self.driver.find_element_by_xpath(ADD_HUB_BUTTON % card_name)
        print('User taps on add')
        add_hub_button.click()

    def search_hub(self, card_name):
        search_field = self.driver.find_element_by_id(SEARCH_FIELD)
        print('User tap on search filed')
        search_field.click()
        search_field.send_keys(card_name)

    def check_added_hub(self, card_name):
        CardsNavigationPage.search_hub(self, card_name)
        if len(self.driver.find_elements_by_xpath(ADD_HUB_BUTTON % card_name)) >= 1:
            print('Hub added')
        else:
            print(self.fail('Hub not added'))

    def cancelSearch(self):
        cancel_button = self.driver.find_element_by_id(CANCEL_SEARCH)
        print('User tap on cancel')
        cancel_button.click()

    def expandHub(self, hub_name):
        card_title = self.driver.find_element_by_name(hub_name)
        print('User expands hub')
        card_title.click()

    def addGhostCard(self, card_name):
        sleep(2)
        add_hub_button = self.driver.find_element_by_xpath(ADD_HUB_BUTTON % card_name)
        print('User taps on add')
        add_hub_button.click()
        notify_button = self.driver.find_element_by_id(NOTIFY_BUTTON)
        print('User tap on Notify button')
        notify_button.click()

    def removeHub(self, card_name):
        card_title = self.driver.find_element_by_id(CARD_TITLE)
        action = TouchAction(self.driver)
        action.long_press(card_title).release().perform()
        delete_hub_button = self.driver.find_element_by_id(DELETE_HUB_BUTTON)
        print('User removes hub')
        delete_hub_button.click()
        print('Check if hub is removed')
        CardsNavigationPage.search_hub(self, card_name)
        add_hub_button = self.driver.find_element_by_xpath(ADD_HUB_BUTTON % card_name)
        if add_hub_button.is_displayed():
            print('%s hub is successfully removed' % card_name)
        else:
            self.fail('%s hub is not removed' % card_name)
        sleep(3)



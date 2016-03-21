from time import sleep
import unittest
from appium.webdriver.common.touch_action import TouchAction
from src.ios.data.bkstg_locators import *


class CardsNavigationPage(unittest.TestCase):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def add_hub(self, card_name):
        add_hub_button = self.driver.find_element_by_xpath(ADD_HUB_BUTTON % card_name.upper())
        print('User taps on %s' % add_hub_button.text)
        add_hub_button.click()

    def search_hub(self, hub_name):
        sleep(2)
        search_field = self.driver.find_element_by_xpath(SEARCH_FIELD)
        search_field.click()
        print('Searching %s hub' % hub_name.upper())
        search_field.send_keys(hub_name.upper())

    def remove_hub(self, card_name):
        card_title = self.driver.find_element_by_name(card_name.upper())
        action = TouchAction(self.driver)
        action.long_press(card_title).release().perform()
        delete_hub_button = self.driver.find_element_by_xpath(DELETE_HUB_BUTTON)
        print('User removes hub')
        delete_hub_button.click()
        print('Check if hub is removed')
        self.search_hub(card_name)
        add_hub_button = self.driver.find_element_by_xpath(ADD_HUB_BUTTON % card_name.upper())
        add_hub_button.is_displayed()
        print('%s hub is successfully removed' % card_name.upper())

    def expand_hub(self):
        card_title = self.driver.find_element_by_xpath(CARD_LAYOUT)
        print('User expands hub')
        card_title.click()

    def add_ghost_hub(self, ghost_hub_name):
        self.search_hub(ghost_hub_name)
        card_title = self.driver.find_element_by_name(ghost_hub_name.upper()).text
        print('Check if ghost card title corresponds search')
        self.assertIn(card_title, ghost_hub_name.upper())
        self.add_hub(ghost_hub_name)
        ghost_card_notify_button = self.driver.find_element_by_xpath(GHOST_CARD_NOTIFY_BUTTON)
        print('User agrees to notify him when this hub will be added')
        ghost_card_notify_button.click()

    def accept_permissions(self):
        i = 0
        for i in range(0, 2):
            notification_ok_button = self.driver.find_elements_by_name(NOTIFICATION_OK_BUTTON)
            if len(notification_ok_button) > 0:
                print('User grants permission access')
                notification_ok_button[0].click()
                i += 1
            else:
                break

    def check_sign_in(self):
        print('Check if user is logged in')
        search_field = self.driver.find_elements_by_xpath(SEARCH_FIELD)
        if len(search_field) >= 1:
            print('User is logged in')
        else:
            self.fail('User is not logged in')




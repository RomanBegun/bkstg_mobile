__author__ = 'Roma'
from time import sleep
import unittest
from src.android.data.bkstg_locators import *


class CommunityPage(unittest.TestCase):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def selectCommunityFilter(self, filter):
        if filter == 'HOT':
            hot_filter = self.driver.find_element_by_name(FILTER_HOT)
            print('User select HOT filter')
            hot_filter.click()
        elif filter == 'NEW':
            new_filter = self.driver.find_element_by_name(FILTER_NEW)
            print('User select NEW filter')
            new_filter.click()
        elif filter == 'NEARBY':
            nearby_filter = self.driver.find_element_by_name(FILTER_NEARBY)
            print('User select NEARBY filter')
            nearby_filter.click()
        elif filter == 'FOLLOWING':
            following_filter = self.driver.find_element_by_name(FILTER_FOLLOWING)
            print('User select FOLLOFING filter')
            following_filter.click()
        else:
            self.fail('Filter not found')
        sleep(5)

    def promotedHashtags(self, number):
            if number == '1':
                promoted_hashtags = self.driver.find_element_by_xpath(PROMOTED_HASHTAGS % "2")
                print('User select first hashtag - %s' % promoted_hashtags.text)
                promoted_hashtags.click()
            elif number == '2':
                promoted_hashtags = self.driver.find_element_by_xpath(PROMOTED_HASHTAGS % "3")
                print('User select second hashtag - %s' % promoted_hashtags.text)
                promoted_hashtags.click()
            elif number == '3':
                promoted_hashtags = self.driver.find_element_by_xpath(PROMOTED_HASHTAGS % "4")
                print('User select third hashtag - %s' % promoted_hashtags.text)
                promoted_hashtags.click()
            elif number == '4':
                promoted_hashtags = self.driver.find_element_by_xpath(PROMOTED_HASHTAGS % "5")
                print('User select four hashtag - %s' % promoted_hashtags.text)
                promoted_hashtags.click()
            elif number == '5':
                promoted_hashtags = self.driver.find_element_by_xpath(PROMOTED_HASHTAGS % "6")
                print('User select fifth hashtag - %s' % promoted_hashtags.text)
                promoted_hashtags.click()
            else:
                self.fail('Undefined hashtags')
            sleep(5)


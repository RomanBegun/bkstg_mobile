__author__ = 'Roma'
from time import sleep
import time
import unittest
from src.android.data.bkstg_locators import *


class HubFeedPage(unittest.TestCase):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def postComment(self, comment):
        timestamp = str(time.time()).split('.')[0]
        for i in range(0, 2):
            self.driver.swipe(200, 600, 200, 200)
            sleep(1)
        comment_button = self.driver.find_element_by_id(COMMENT_BUTTON)
        print('User taps add comment button')
        comment_button.click()
        comment_field = self.driver.find_element_by_id(COMMENT_FIELD)
        comment_field.send_keys(comment + '-%s' % timestamp)
        print('User adds comment - "%s"' % comment)
        send_comment_button = self.driver.find_element_by_id(SEND_COMMENT_BUTTON)
        print('User posts comment')
        send_comment_button.click()
        print('Checking if comment is added in the feed...')
        comment_value = comment + '-%s' % timestamp
        comment_text = self.driver.find_element_by_xpath(COMMENT_TEXT % comment_value)
        if comment_text.is_displayed():
            print('Comment "%s" is successfully added' % comment_value)
        else:
            self.fail('Comment is not added')
        sleep(2)
        self.driver.back()

    def postLike(self):
        for i in range(0, 2):
            self.driver.swipe(200, 600, 200, 200)
            sleep(1)
        like_count = self.driver.find_element_by_id(LIKE_COUNT)
        like_before = int(like_count.text)
        like_button = self.driver.find_element_by_id(LIKE_BUTTON)
        print('User tap on like button')
        like_button.click()
        sleep(2)
        like_after = int(like_count.text)
        if like_after > like_before:
            print('like added')
        else:
            print('Like not added')

    def postUnlike(self):
        like_count = self.driver.find_element_by_id(LIKE_COUNT)
        like_before = int(like_count.text)
        like_button = self.driver.find_element_by_id(LIKE_BUTTON)
        print('User tap on like button')
        like_button.click()
        sleep(2)
        like_after = int(like_count.text)
        if like_after < like_before:
            print('like removed')
        else:
            print('Like not removed')

    def openCreationTools(self):
        creation_tools_button = self.driver.find_element_by_id(CREATION_TOOLS_BUTTON)
        print('User tap on Creations tool button')
        creation_tools_button.click()
        if len(self.driver.find_elements_by_xpath('//android.widget.TextView[@text="Try Again"]')) >= 1:
            self.driver.find_element_by_xpath('//android.widget.TextView[@text="Try Again"]').click()
        if not len(self.driver.find_elements_by_id(TEXT_INPUT_VIEW)) >= 1:
            self.fail('Creation tools page not opened')

    def uploadPostMessage(self):
        sleep(3)
        upload_post_message = self.driver.find_element_by_id(UPLOAD_POST_MESSAGE)
        if 'POST UPLOAD SUCCESSFUL' or 'HOLD' in upload_post_message.text:
            print('Post successful create')
        else:
            self.fail('Post not created')

    def openBkstgSubMenu(self):
        bkstg_sub_menu = self.driver.find_element_by_id(BKSTG_SUB_MENU)
        print('User open Bkstg Sub menu')
        bkstg_sub_menu.click()
        sleep(1)

    def selectSubMenuItem(self, item):
        if item == 'Feed':
            bkstg_sum_menu_item = self.driver.find_element_by_xpath(BKSTG_SUB_MENU_ITEM % "1")
            print('User select "%s"' % item)
            bkstg_sum_menu_item.click()
        elif item == 'Community':
            bkstg_sum_menu_item = self.driver.find_element_by_xpath(BKSTG_SUB_MENU_ITEM % "2")
            print('User select "%s"' % item)
            bkstg_sum_menu_item.click()
        elif item == 'Photos':
            bkstg_sum_menu_item = self.driver.find_element_by_xpath(BKSTG_SUB_MENU_ITEM % "3")
            print('User select "%s"' % item)
            bkstg_sum_menu_item.click()
        elif item == 'Videos':
            bkstg_sum_menu_item = self.driver.find_element_by_xpath(BKSTG_SUB_MENU_ITEM % "4")
            print('User select "%s"' % item)
            bkstg_sum_menu_item.click()
        elif item == 'Store':
            bkstg_sum_menu_item = self.driver.find_element_by_xpath(BKSTG_SUB_MENU_ITEM % "5")
            print('User select "%s"' % item)
            bkstg_sum_menu_item.click()
        elif item == 'Tickets':
            bkstg_sum_menu_item = self.driver.find_element_by_xpath(BKSTG_SUB_MENU_ITEM % "6")
            print('User select "%s"' % item)
            bkstg_sum_menu_item.click()
        elif item == 'Music':
            sleep(1)
            self.driver.swipe(550, 1650, 300, 1650)
            sleep(1)
            bkstg_sum_menu_item = self.driver.find_element_by_xpath(BKSTG_SUB_MENU_ITEM % "7")
            print('User select "%s"' % item)
            bkstg_sum_menu_item.click()
        else:
            self.fail('Item not found')
        # if self.driver.find_element_by_xpath(VERIFY_SUB_MENU_ITEM).text == item:
        #     print('User opened "%s" page' % item)
        # else:
        #     self.fail('Page is not opened')
        self.openBkstgSubMenu()

    def chooseShareMethod(self, share):
        share_button = self.driver.find_element_by_id(SHARE_BUTTON)
        print('User click on share button')
        share_button.click()
        share_way = self.driver.find_element_by_xpath(SHARE_WAY % share)
        print('User select - "%s" method for share' % share)
        share_way.click()
        sleep(5)




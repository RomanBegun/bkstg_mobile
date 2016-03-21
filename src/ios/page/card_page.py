import datetime
from selenium.webdriver import ActionChains
import unittest
from src.ios.data.bkstg_locators import *


class CardPage(unittest.TestCase):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def post_comment(self, comment):
        self.driver.swipe(100, 300, 100, 100)
        time = str(datetime.datetime.now()).split('.')[0]
        add_comment_button = self.driver.find_element_by_xpath(ADD_COMMENT_BUTTON)
        print('User taps add comment button')
        add_comment_button.click()
        comment_field = self.driver.find_element_by_xpath(COMMENT_FIELD)
        comment_field.set_value(comment + ' %s' % time)
        print('User adds comment - "%s"' % comment)
        post_comment_button = self.driver.find_element_by_xpath(POST_COMMENT_BUTTON)
        print('User posts comment')
        post_comment_button.click()
        print('Checking if comment is added in the feed...')
        comment_value = comment + ' %s' % time
        comment_text = self.driver.find_element_by_xpath(COMMENT_TEXT % comment_value)
        if comment_text.is_displayed():
            print('Comment "%s" is successfully added' % comment_value)
        else:
            self.fail('Comment is not added')
        self.driver.implicitly_wait(5)
        close_comments_button = self.driver.find_element_by_xpath(CLOSE_COMMENTS_BUTTON)
        print('Closing comment section')
        close_comments_button.click()

    def like_post(self):
        no_likes_title = self.driver.find_elements_by_xpath(NO_LIKES_TITLE)
        # Check if post have some likes
        if len(no_likes_title) < 1:
            likes_counter = self.driver.find_element_by_xpath(LIKES_COUNTER)
            likes_counter.click()
            print('Post likes amount - %s' % likes_counter.text)
            liked_counter_value = int(likes_counter.text) + 1
            action = ActionChains(self.driver)
            action.move_to_element_with_offset(likes_counter, 0, -20).click().perform()
            print('User taps on like button')
            print('Checking if likes counter is updated...')
            print('Post new likes amount - %s' % likes_counter.text)
            self.assertIn(str(liked_counter_value), likes_counter.text)
        else:
            no_likes_text = self.driver.find_element_by_xpath(NO_LIKES_TITLE)
            no_likes_view = self.driver.find_element_by_xpath(NO_LIKES_VIEW)
            print('Nobody likes this post')
            print(no_likes_text.text)
            no_likes_view.click()
            print('User scrolls to likes block')
            action = ActionChains(self.driver)
            print('User taps on like button')
            action.move_to_element_with_offset(no_likes_text, -10, 0).click().perform()
            print('Checking if likes counter is updated...')
            self.driver.implicitly_wait(5)
            likes_counter = self.driver.find_element_by_xpath(LIKES_COUNTER)
            print('Post new likes amount - %s' % likes_counter.text)
            #self.assertIn('1', likes_counter.text)

    def unlike_post(self):
        likes_counter = self.driver.find_element_by_xpath(LIKES_COUNTER)
        likes_counter.click()
        print('Post likes amount - %s' % likes_counter.text)
        liked_counter_value = int(likes_counter.text) - 1
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(likes_counter, 0, -20).click().perform()
        print('User taps on unlike button')
        print('Checking if likes counter is updated...')
        print('Post new likes amount - %s' % likes_counter.text)
        self.assertIn(str(liked_counter_value), likes_counter.text)

    def open_hub_section(self, section):
        bkstg_button = self.driver.find_element_by_name(BKSTG_BUTTON)
        print('User taps on bkstg button')
        bkstg_button.click()
        section_button = self.driver.find_element_by_name(section.upper())
        print('User taps on %s section button' % section)
        section_button.click()







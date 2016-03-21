import unittest
from time import sleep
import time
from src.android.data.bkstg_locators import *


class CreationToolsPage(unittest.TestCase):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def addTextInView(self):
        timestamp = str(time.time()).split('.')[0]
        text = 'Creation tools test %s' % timestamp
        text_input_view = self.driver.find_element_by_id(TEXT_INPUT_VIEW)
        print('User tap on input text view')
        text_input_view.click()
        print('User entered text - "%s"' % text)
        text_input_view.send_keys(text)
        self.driver.back()

    def addLastGalleryPhoto(self):
        last_gallery_photo = self.driver.find_element_by_xpath(LAST_GALLERY_PHOTO)
        print('User add last gallery photo')
        last_gallery_photo.click()

    def addText(self):
        timestamp = str(time.time()).split('.')[0]
        text = 'Creation tools test %s' % timestamp
        add_text_view = self.driver.find_element_by_id(ADD_TEXT)
        print('User entered text - "%s"' % text)
        add_text_view.send_keys(text)
        self.driver.back()

    def makePhoto(self):
        camera_preview = self.driver.find_element_by_xpath(CAMERA_PREVIEW)
        print('User tap on Camera Preview')
        camera_preview.click()
        sleep(1)
        self.driver.swipe(200, 400, 200, 200)
        sleep(1)
        make_photo_button = self.driver.find_element_by_id(MAKE_PHOTO_BUTTON)
        print('User click on make photo button')
        make_photo_button.click()

    def clickPost(self):
        self.driver.swipe(200, 1500, 200, 1000)
        sleep(1)
        post_button = self.driver.find_element_by_id(POST_BUTTON)
        print('User tap on Post button')
        post_button.click()
        sleep(3)

    def openGallery(self):
        media_gallery = self.driver.find_element_by_xpath(MEDIA_GALLERY)
        print('User click on media gallery')
        media_gallery.click()

    def chooseMediaContent(self, item):
        if item == 'Photo':
            select_photo = self.driver.find_element_by_xpath(SELECT_PHOTO)
            print('User select Photo')
            select_photo.click()
        elif item == 'Contacts':
            select_contacts = self.driver.find_element_by_xpath(SELECT_CONTACTS)
            print('User select Contacts')
            select_contacts.click()
        elif item == 'Music':
            select_music = self.driver.find_element_by_xpath(SELECT_MUSIC)
            print('User select Music')
            select_music.click()

    def chooseMediaItem(self):
        open_native_photo_gallery = self.driver.find_element_by_xpath(OPEN_NATIVE_PHOTO_GALLERY)
        print('User open native photo gallery')
        open_native_photo_gallery.click()
        select_item = self.driver.find_element_by_xpath(SELECT_PHOTO_ITEM_FROM_GALLERY)
        print('User select item from native gallery')
        select_item.click()

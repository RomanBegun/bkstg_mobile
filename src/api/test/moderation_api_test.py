import logging
import unittest
import requests

from random import randint

from src.api.helpers.unique_gen import *
from src.api.setup.preconditions import Preconditions
from src.api.urls.api_urls import *


class ModerationApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        global auth, base_url, hub_id, headers

        auth = Preconditions()
        base_url = auth.env.base_url

        auth.log_in()
        headers = {"Authorization": "Token %s" % auth.token}

        auth.create_hub(headers)
        hub_id = auth.hub_id

        global item_content_id, item_content_id_2, item_content_id_3

        auth.add_community_inappropriate_post(hub_id, 'boobs')
        item_content_id = auth.inappropriate_community_post_id

        auth.add_community_inappropriate_post(hub_id, 'boobs')
        item_content_id_2 = auth.inappropriate_community_post_id

        auth.add_community_inappropriate_post(hub_id, 'boobs')
        item_content_id_3 = auth.inappropriate_community_post_id

    @classmethod
    def tearDownClass(cls):

        # Delete hub
        print('Delete hub...')
        r = requests.delete(base_url + HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        if '20' not in str(r.status_code):
            raise AssertionError(r.status_code)

    def test_add_remove_inappropriate_word(self):

        marker = generate_unique()
        inappropriate_word = 'f*ck-%s' % marker
        inappropriate_data = '{"word" :"%s"}' % inappropriate_word

        # Add inappropriate word to list
        print('Add inappropriate word to hub...')
        r = requests.post(base_url + INAPPROPRIATE_WORDS_LIST % hub_id, data=inappropriate_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['word'] != '%s' % inappropriate_word:
            self.fail('Wrong response.')

        word_id = r.json()['id']

        # Remove inappropriate word from list
        print('Delete inappropriate word...')
        url = base_url + INAPPROPRIATE_WORD % (hub_id, word_id)
        r = requests.delete(url, data=inappropriate_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

    def test_get_inappropriate_words_list(self):

        rnd = randint(100, 9999)
        inappropriate_word = 'f*ck-%s' % rnd
        inappropriate_data = '{"word" :"%s"}' % inappropriate_word

        print('Add inappropriate word to hub...')
        r = requests.post(base_url + INAPPROPRIATE_WORDS_LIST % hub_id, data=inappropriate_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['word'] != '%s' % inappropriate_word:
            self.fail('Wrong response.')

        # Get inappropriate words list
        print('Get list of inappropriate words for hub...')
        r = requests.get(base_url + INAPPROPRIATE_WORDS_LIST % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['results'][0]['id'] or not r.json()['results'][0]['word']:
            self.fail('Wrong response.')

    @unittest.skip
    def test_get_reported_content(self):

        # Get reported content
        print('Get list of reported content for hub...')
        r = requests.get(base_url + REPORTED_CONTENT % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['results'][0]['status'] != 'review':
            self.fail('Wrong response.')

    @unittest.skip
    def test_get_inappropriate_item(self):

        item_content_type = 'community:post'

        # Get inappropriate item
        print('Get inappropriate item...')
        url = base_url + INAPPROPRIATE_ITEM % (hub_id, item_content_type, item_content_id)
        r = requests.get(url, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['content_id'] == item_content_id:
            self.fail('Wrong response.')

    @unittest.skip
    def test_delete_inappropriate_item(self):

        item_content_type = 'community:post'

        # Delete inappropriate item
        print('Delete inappropriate item')
        url = base_url + INAPPROPRIATE_ITEM % (hub_id, item_content_type, item_content_id_2)
        r = requests.delete(url, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

    @unittest.skip
    def test_mark_inappropriate_post(self):

        item_content_type = 'community:post'
        url = base_url + INAPPROPRIATE_ITEM % (hub_id, item_content_type, item_content_id_3)

        # Mark inappropriate post in Save
        print('Mark inappropriate post in save')
        status_data = '{"status": "safe"}'
        r = requests.put(url, data=status_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['status'] == 'safe':
            self.fail('Wrong response.')

        # Mark inappropriate post in Review
        print('Mark inappropriate post in review')
        status_data_2 = '{"status": "review"}'
        r = requests.put(url, data=status_data_2, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['status'] == 'review':
            self.fail('Wrong response.')

        # Mark inappropriate post in Deleted
        print('Mark inappropriate post in deleted')
        status_data_3 = '{"status": "deleted"}'
        r = requests.put(url, data=status_data_3, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['status'] == 'deleted':
            self.fail('Wrong response.')

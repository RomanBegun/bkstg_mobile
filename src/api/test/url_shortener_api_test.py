import json
import logging
import unittest
import requests

from src.api.setup.preconditions import Preconditions
from src.api.urls.api_urls import *


class UrlShortenerApiTest(unittest.TestCase):

    @classmethod    
    def setUpClass(cls):
        
        global auth, base_url, headers, hub_id, user_id, post_id
        
        auth = Preconditions()
        base_url = auth.env.base_url

        auth.log_in()
        user_id = auth.user_id
        headers = {"Authorization": "Token %s" % auth.token, "Content-Type": "application/json"}

        auth.create_hub(headers)
        hub_id = auth.hub_id

        # auth.create_feed_post(headers, hub_id)
        # feed_post_id = auth.feed_post_id

        auth.create_community_post(headers, hub_id)
        post_id = auth.community_post_id
        
        global short_url

        short_url = auth.short_url

    @classmethod
    def tearDownClass(cls):

        # Delete hub
        print('Delete hub...')
        r = requests.delete(base_url + HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        if '20' not in str(r.status_code):
            raise AssertionError(r.status_code)

    def test_create_short_url(self):
        
        url_data = json.dumps({'url': '%s' % short_url})

        # Crate short url
        print("Create short url for feed post...")
        r = requests.post(base_url + URL_SHORTENER, data=url_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if 'bkstg.com' not in r.json()['url'] or not r.json()['code']:
            self.fail('Wrong response.')

    def test_get_params_by_code(self):

        url_data = json.dumps({
            'url': '%s' % short_url,
            'data': {
                'hub_id': "%s" % hub_id,
                'post_id': '%s' % post_id
            }
        })

        # Crate short url
        print("Create short url for feed post...")
        r = requests.post(base_url + URL_SHORTENER, data=url_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if 'bkstg.com' not in r.json()['url'] or not r.json()['code']:
            self.fail('Wrong response.')

        code = r.json()['code']

        # Get params by code
        print("Get params by code...")
        r = requests.get(base_url + URL_SHORTENER_PARAMS % code, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if short_url not in r.json()['url'] and hub_id != r.json()['hub_id'] and post_id != r.json()['post_id']:
            self.fail('Wrong response.')

import unittest
import requests
import logging

from src.api.setup.preconditions import Preconditions
from src.api.urls.api_urls import *


class SettingsApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        global auth, base_url, headers, hub_id

        auth = Preconditions()
        base_url = auth.env.base_url

        auth.log_in()
        headers = {"Authorization": "Token %s" % auth.token}

        auth.create_hub(headers)
        hub_id = auth.hub_id

    @classmethod
    def tearDownClass(cls):

        # Delete hub
        print('Delete hub...')
        r = requests.delete(base_url + HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        if '20' not in str(r.status_code):
            raise AssertionError(r.status_code)

    def test_get_settings_for_application(self):

        # Get application settings
        print('Get application settings...')
        r = requests.get(base_url + SETTINGS_APPLICATION, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        if not r.json()['accounts'] or not r.json()['media'] or not r.json()['system']:
            self.fail('Wrong response.')

    def test_get_settings_for_hub(self):

        # Get settings for hub
        print('Get settings for hub...')
        r = requests.get(base_url + SETTINGS_HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        if not r.json()['accounts'] or not r.json()['media'] or not r.json()['system']:
            self.fail('Wrong response.')

import json
import unittest
import requests
import logging

from src.api.urls.api_urls import *
from src.api.setup.preconditions import Preconditions


class StaticPagesApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        global auth, base_url, headers
        auth = Preconditions()
        auth.log_in()
        headers = {"Authorization": "Token %s" % auth.token}
        base_url = auth.env.base_url

    def test_get_terms_and_conditions_page(self):

        # Get Terms and Conditions page
        print("Get 'Terms and Conditions' page...")
        r = requests.get(base_url + STATIC_TC_PAGE)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        # No page content on Dev 2.
        # page_content = str(r.content)
        # if 'There will be Terms and conditions.' not in page_content:
        #     self.fail('Wrong response.')

    @unittest.skip
    def test_post_terms_and_conditions_page(self):

        raw = {"content": "There will be Terms and conditions."}
        payload = json.dumps(raw)

        # Post Terms and Conditions page
        print("Post 'Terms and Conditions' page...")
        r = requests.post(base_url + STATIC_TC_PAGE, data=payload, headers=headers)
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

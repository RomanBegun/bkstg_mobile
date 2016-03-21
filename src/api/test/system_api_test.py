import unittest
import requests
import logging

from src.api.setup.preconditions import Preconditions


class SystemApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        global auth, base_url

        auth = Preconditions()
        base_url = auth.env.base_url

    def test_heartbeat(self):

        # Get system heartbeat
        print('Get system heartbeat...')
        r = requests.get(base_url[:-4] + '/heartbeat')
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.text != 'Up and running.':
            self.fail('Wrong response.')

import logging
import unittest
import json
import requests

from src.api.helpers.unique_gen import *
from src.api.setup.preconditions import Preconditions
from src.api.setup.test_data import TestData
from src.api.urls.api_urls import *


class AuthApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        global auth, base_url, headers

        auth = Preconditions()
        base_url = auth.env.base_url

        auth.log_in()
        headers = {"Authorization": "Token %s" % auth.token}

        global new_user_id, new_user_headers, new_user_name, new_user_email

        auth.create_user()
        new_user_id = auth.new_user_id
        new_user_name = auth.new_user_name
        new_user_email = auth.new_user_email
        new_user_headers = {"Authorization": "Token %s" % auth.new_user_token}

    def test_sign_up(self):

        marker = generate_unique()
        signup_data = {"username": "test-%s" % marker,
                       "password": "qqqqqqqq",
                       "email": "bkstg.test-API%s@stub.bkstg.com" % marker,
                       "device_type": "ios",
                       "device_id": "4B8F7BDD-8D8D-40A2-9412-8A5ECD5BF1A3",
                       "birthday": "1991-08-08",
                       "full_name": "API Test %s" % marker
                       }
        payload = json.dumps(signup_data)
        
        # Register user
        print('Register user...')
        r = requests.post(base_url + AUTH_SIGN_UP, data=payload)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['token']:
            self.fail('Token is missing.')

        reg_token = r.json()['token']

        print('Check account info...')
        r = requests.get(base_url + ACCOUNT_USER, headers={"Authorization": 'Token %s' % reg_token})
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['username'] != 'test-%s' % marker or r.json()['birthday'] != '1991-08-08':
            self.fail('Wrong user info')

    def test_log_in(self):

        login_payload = '{"email": "%s", "password": "%s"}' % (TestData.email, TestData.password)

        # Log in
        print('Log in...')
        r = requests.post(base_url + AUTH_LOGIN, data=login_payload)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['token']:
            self.fail('Token is missing')
        self.token = r.json()['token']

    def test_log_out(self):

        # Log out
        print('Log out...')
        r = requests.post(base_url + AUTH_LOGOUT, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

    def test_forgot_password(self):

        raw = {"email": "%s" % TestData.email}
        payload = json.dumps(raw)

        # Forgot password
        print('Forgot password...')
        r = requests.post(base_url + AUTH_FORGOT_PASSWORD, headers=headers, data=payload)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

    def test_change_password(self):

        marker = generate_unique()
        email = 'bkstg.test-API%s@stub.bkstg.com' % marker
        new_password = '12345678'
        signup_data = {"username": "test-%s" % marker,
                       "password": "qqqqqqqq",
                       "email": email,
                       "device_type": "ios",
                       "device_id": "4B8F7BDD-8D8D-40A2-9412-8A5ECD5BF1A3",
                       "birthday": "1991-08-08",
                       "full_name": "API Test %s" % marker
                       }
        payload = json.dumps(signup_data)

        print('Register user...')
        r = requests.post(base_url + AUTH_SIGN_UP, data=payload)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['token']:
            self.fail('Token is missing.')

        reg_token = r.json()['token']
        passwords = {"old_password": "qqqqqqqq",
                     "new_password": new_password
                     }
        payload = json.dumps(passwords)

        # Change password
        print('Change password...')
        url = base_url + AUTH_CHANGE_PASSWORD
        r = requests.put(url, data=payload, headers={"Authorization": 'Token %s' % reg_token})
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        print('Log out...')
        r = requests.post(base_url + AUTH_LOGOUT, headers={"Authorization": 'Token %s' % reg_token})
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        login_payload = '{"email": "%s", "password": "%s"}' % (email, new_password)

        print('Log in...')
        r = requests.post(base_url + AUTH_LOGIN, data=login_payload)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

    def test_check_name(self):

        marker = generate_unique()
        username = "API_Test-%s" % marker
        
        # Check unique name        
        print('Check unique username...')
        r = requests.get(base_url + AUTH_CHECK_NAME + '?username=%s' % username)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        username = ''

        # Check empty username
        print('Check empty username...')
        r = requests.get(base_url + AUTH_CHECK_NAME + '?username=%s' % username)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('40', str(r.status_code), msg=logging.debug(r.text))
        if 'Username is not specified.' not in r.json()['errors']['username']:
            self.fail('Wrong response.')

        username = '12 3'

        # Check invalid username
        print('Check invalid username...')
        r = requests.get(base_url + AUTH_CHECK_NAME + '?username=%s' % username)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('40', str(r.status_code), msg=logging.debug(r.text))
        if "Username can't contain # and @ chars and whitespaces." not in r.json()['errors']['username']:
            self.fail('Wrong response.')

        username = "admin"

        # Check existing name
        print('Check existing username...')
        r = requests.get(base_url + AUTH_CHECK_NAME + '?username=%s' % username)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('40', str(r.status_code), msg=logging.debug(r.text))
        if 'Shoot. Another fan grabbed that name. Try again?' not in r.json()['errors']['username']:
            self.fail('Wrong response.')

    def test_check_email(self):

        marker = generate_unique()
        email = "bkstg.test-API%s@stub.bkstg.com" % marker

        # Check unique email
        print('Check unique email...')
        r = requests.get(base_url + AUTH_CHECK_EMAIL + '?email=%s' % email)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        email = ''

        # Check empty email
        print('Check empty email...')
        r = requests.get(base_url + AUTH_CHECK_EMAIL + '?email=%s' % email)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('40', str(r.status_code), msg=logging.debug(r.text))
        if 'You must supply a email.' not in r.json()['errors']['email']:
            self.fail('Wrong response.')

        email = '123'

        # Check invalid email
        print('Check invalid email...')
        r = requests.get(base_url + AUTH_CHECK_EMAIL + '?email=%s' % email)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('40', str(r.status_code), msg=logging.debug(r.text))
        if 'Invalid email address.' not in r.json()['errors']['email']:
            self.fail('Wrong response.')

        email = TestData.email

        # Check existing email
        print('Check existing email...')
        r = requests.get(base_url + AUTH_CHECK_EMAIL + '?email=%s' % email)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('40', str(r.status_code), msg=logging.debug(r.text))
        if 'Email address already being used' not in r.json()['message']:
            self.fail('Wrong response.')

    def test_fb_log_in(self):

        # Create new Facebook user
        print("Create new Facebook user...")
        url = 'https://graph.facebook.com/v2.5/%s/accounts/test-users?access_token=%s'
        r = requests.post(url % (TestData.facebook_app_id, TestData.access_token))
        print('Status code - %s' % r.status_code, '\n')

        fb_access_token = r.json()["access_token"]

        # Facebook log in
        print('Log in via Facebook...')
        fb_data = json.dumps({"fb_token": fb_access_token})
        r = requests.post(base_url + AUTH_FB_LOGIN, data=fb_data)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['user_exists'] == False:
            self.fail('User is not logged in via Facebook.')

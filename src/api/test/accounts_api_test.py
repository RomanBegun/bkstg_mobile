import json
import logging
import unittest
import requests

from src.api.helpers.unique_gen import *
from src.api.setup.test_data import TestData
from src.api.urls.api_urls import *
from src.api.setup.preconditions import Preconditions


class AccountsApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        global auth, base_url, headers, hub_id, user_id

        auth = Preconditions()
        base_url = auth.env.base_url

        auth.log_in()
        user_id = auth.user_id
        headers = {"Authorization": "Token %s" % auth.token, "BKSTG_DISABLE_CACHE": "True"}

        auth.create_hub(headers)
        hub_id = auth.hub_id

        global new_user_id, new_user_headers, new_user_name, new_user_email

        auth.create_user()
        new_user_id = auth.new_user_id
        new_user_name = auth.new_user_name
        new_user_email = auth.new_user_email
        new_user_headers = {"Authorization": "Token %s" % auth.new_user_token, "BKSTG_DISABLE_CACHE": "True"}

        global new_user_headers_2, new_user_id_2

        auth.create_user()
        new_user_id_2 = auth.new_user_id
        new_user_headers_2 = {"Authorization": "Token %s" % auth.new_user_token, "BKSTG_DISABLE_CACHE": "True"}

        global new_user_email_3, new_user_id_3, new_user_headers_3

        auth.create_user()
        new_user_id_3 = auth.new_user_id
        new_user_email_3 = auth.new_user_email
        new_user_headers_3 = {"Authorization": "Token %s" % auth.new_user_token, "BKSTG_DISABLE_CACHE": "True"}

        global new_user_email_4, new_user_id_4, new_user_headers_4

        auth.create_user()
        new_user_id_4 = auth.new_user_id
        new_user_email_4 = auth.new_user_email
        new_user_headers_4 = {"Authorization": "Token %s" % auth.new_user_token, "BKSTG_DISABLE_CACHE": "True"}

    @classmethod
    def tearDownClass(cls):

        # Delete hub
        print('Delete hub...')
        r = requests.delete(base_url + HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        if '20' not in str(r.status_code):
            raise AssertionError(r.status_code)

    def test_get_my_profile(self):

        # Get my profile
        print('Get my profile...')
        r = requests.get(base_url + ACCOUNT_USER, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['email'] != TestData.email:
            self.fail('Wrong user info.')

    def test_get_user_profile_by_id(self):

        # Get user profile by id
        print('Get user profile by id...')
        r = requests.get(base_url + ACCOUNT_PROFILE % new_user_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['id'] != new_user_id:
            self.fail('Wrong response.')

    def test_get_user_profile_by_name(self):

        # Get user profile by name
        print('Get user profile by name...')
        r = requests.get(base_url + ACCOUNT_PROFILE % new_user_name, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['username'] != new_user_name:
            self.fail('Wrong response.')

    def test_get_user_profile_by_email(self):

        # Get user profile by email
        print('Get user profile by email...')
        r = requests.get(base_url + ACCOUNT_PROFILE % new_user_email_3, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['id'] != new_user_id_3:
            self.fail('Wrong response.')

    def test_edit_profile(self):

        marker = generate_unique()
        edit_account_payload = {"first_name": "Test %s" % marker,
                                "last_name": "API",
                                "birthday": "1990-08-08",
                                "phone": "+222222222222",
                                "street": "Edited",
                                "state": "California",
                                "country": "USA",
                                "city": "Los Angeles",
                                "public_address": "Public St. 21",
                                "private_address": "Private St. 99",
                                "bio": "edited bio",
                                "gender": "male",
                                "zip": "12345",
                                "apartment": "22"
                                }
        payload = json.dumps(edit_account_payload)

        # Edit my profile
        print('Edit account info...')
        url = base_url + ACCOUNT_USER
        r = requests.put(url, data=payload, headers=new_user_headers_2)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if info is updated
        print('Check if info is updated in profile...')
        r = requests.get(base_url + ACCOUNT_USER, headers=new_user_headers_2)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not edit_account_payload.items() <= r.json().items():
            self.fail('Wrong response.')

    @unittest.skip
    def test_edit_profile_by_id(self):

        marker = generate_unique()
        edit_account_payload = {"first_name": "Test %s" % marker,
                                "last_name": "API",
                                "birthday": "1990-08-08",
                                "phone": "+222222222222",
                                "street": "Edited",
                                "state": "California",
                                "country": "USA",
                                "city": "Los Angeles",
                                "public_address": "Public St. 21",
                                "private_address": "Private St. 99",
                                "bio": "edited bio",
                                "gender": "male",
                                "zip": "12345",
                                "apartment": "22"
                                }
        payload = json.dumps(edit_account_payload)

        # Edit user profile by id
        print('Edit account info...')
        url = base_url + ACCOUNT_PROFILE
        r = requests.put(url % new_user_id_2, data=payload, headers=new_user_headers_2)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if info is updated
        print('Check if info is updated in profile...')
        r = requests.get(base_url + ACCOUNT_PROFILE % new_user_id_2, headers=new_user_headers_2)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not edit_account_payload.items() <= r.json().items():
            self.fail('Wrong response.')

    def test_get_my_subscriptions(self):

        # Subscribe to hub as admin
        print('Subscribe to hub as new user...')
        r = requests.post(base_url + ACCOUNT_SUBSCRIBE_HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Get list of hubs I subscribed to
        print('Get list of subscriptions...')
        r = requests.get(base_url + ACCOUNT_SUBSCRIPTIONS, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if user is subscribed to hub
        subscriptions_len = len(r.json()['results'])
        self.subscriptions_count = ''
        for i in range(subscriptions_len):
            if r.json()['results'][i]['id'] == hub_id:
                self.subscriptions_count = r.json()['results'][i]['subscriptions_count']
        if self.subscriptions_count < 0 or self.subscriptions_count == '':
            self.fail('Wrong response.')

        # Unsubscribe from hub
        print('Unsubscribe from hub...')
        r = requests.delete(base_url + ACCOUNT_SUBSCRIBE_HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

    def test_get_user_subscriptions(self):

        # Subscribe to hub as new user
        print('Subscribe to hub as new user...')
        r = requests.post(base_url + ACCOUNT_SUBSCRIBE_HUB % hub_id, headers=new_user_headers_3)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Get list of hubs user subscribed to
        print('Get list of subscriptions for user...')
        r = requests.get(base_url + ACCOUNT_USER_SUBSCRIPTIONS % new_user_id_3, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if user is subscribed to hub
        subscriptions_len = len(r.json()['results'])
        self.subscriptions_count = ''
        for i in range(subscriptions_len):
            if r.json()['results'][i]['id'] == hub_id:
                self.subscriptions_count = r.json()['results'][i]['subscriptions_count']
        if self.subscriptions_count < 0 or self.subscriptions_count == '':
            self.fail('Wrong response.')

        # Unsubscribe from hub
        print('Unsubscribe from hub...')
        r = requests.delete(base_url + ACCOUNT_SUBSCRIBE_HUB % hub_id, headers=new_user_headers_3)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

    def test_subscribe_unsubscribe_hub(self):

        # Create new hub
        auth.create_hub(headers)
        new_hub_id = auth.hub_id

        # Subscribe to hub
        print('Subscribe to hub ...')
        r = requests.post(base_url + ACCOUNT_SUBSCRIBE_HUB % new_hub_id, headers=new_user_headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Checking if user is subscribed to hub
        print('Check if user is subscribed to hub...')
        r = requests.get(base_url + ACCOUNT_SUBSCRIPTIONS, headers=new_user_headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        hubs_len = len(r.json()['results'])
        self.subscribed_hub_id = ''
        for i in range(hubs_len):
            if r.json()['results'][i]['id'] == new_hub_id:
                self.subscribed_hub_id = new_hub_id
        if self.subscribed_hub_id != new_hub_id:
                self.fail('User is not subscribed to hub.')

        # Unsubscribe from hub
        print('Unsubscribe from hub...')
        r = requests.delete(base_url + ACCOUNT_SUBSCRIBE_HUB % new_hub_id, headers=new_user_headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Checking if user is unsubscribed from hub
        print('Checking if user is unsubscribed from hub...')
        r = requests.get(base_url + ACCOUNT_SUBSCRIPTIONS, headers=new_user_headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if len(r.json()['results']) >= hubs_len:
            self.fail('User is not unsubscribed from hub.')

        # Delete hub
        auth.delete_hub(headers, new_hub_id)

    def test_follow_unfollow_user(self):

        # Create follow relation
        print('Follow user...')
        r = requests.post(base_url + ACCOUNT_FOLLOW_USER % new_user_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if user is displayed in followers
        print('Check if user is added as follower...')
        r = requests.get(base_url + ACCOUNT_FOLLOWERS % new_user_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['results'][0]['user']['id'] != user_id:
            self.fail('User is not in followers list.')

        # Delete follow relation
        print('Unfollow user...')
        r = requests.delete(base_url + ACCOUNT_FOLLOW_USER % new_user_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if user is removed from followers
        print('Check if user is removed from followers...')
        r = requests.get(base_url + ACCOUNT_FOLLOWERS % new_user_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['results']:
            self.fail('User is not removed from followers list.')

    def test_get_followers_list(self):

        print('Follow user...')
        r = requests.post(base_url + ACCOUNT_FOLLOW_USER % new_user_id_2, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Get followers list
        print('Get followers list...')
        r = requests.get(base_url + ACCOUNT_FOLLOWERS % new_user_id_2, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['results'][0]['user']['id']:
            self.fail('Wrong response.')

    def test_get_following_list(self):

        # Follow new_user2 by new_user1
        print('Follow user...')
        r = requests.post(base_url + ACCOUNT_FOLLOW_USER % new_user_id_2, headers=new_user_headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if user1 is following user2
        print('Get following list...')
        r = requests.get(base_url + ACCOUNT_FOLLOWING % new_user_id, headers=new_user_headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        following_len = len(r.json()['results'])
        self.following_id = ''
        for i in range(following_len):
            if r.json()['results'][i]['user']['id'] == new_user_id_2:
                self.following_id = new_user_id_2
        if self.following_id != new_user_id_2:
            self.fail('Wrong response.')

    def test_get_user_permission_groups_by_app(self):

        # Get user permission groups
        print('Getting user permission groups...')
        r = requests.get(base_url + ACCOUNT_USER_PERMISSION_GROUPS % (TestData.admin_id, 'app'), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['results'][0]['id'] or not r.json()['results'][0]['title']:
            self.fail('Wrong response.')

    def test_get_user_permission_groups_by_hub_id(self):

        # Get user permission groups
        print('Getting user permission groups...')
        r = requests.get(base_url + ACCOUNT_USER_PERMISSION_GROUPS % (TestData.admin_id, hub_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['results'][0]['id'] or not r.json()['results'][0]['title']:
            self.fail('Wrong response.')

    def test_assign_delete_permission_group(self):

        marker = generate_unique()
        group_name = 'Auto API permission group %s' % marker
        permission_group_data = '{"title": "%s", "scope":"app"}' % group_name

        # Create new permission group
        print('Create permission group...')
        r = requests.post(base_url + PERMISSION_GROUPS_LIST, data=permission_group_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['title'] != group_name or r.json()['scope'] != 'app':
            self.fail('Wrong response.')

        group_id = r.json()['id']
        scope = r.json()['scope']

        # Assign permission group to user
        print('Assign permission group to user...')
        user_permission_url = base_url + ACCOUNT_USER_PERMISSION_GROUP_RELATION % (new_user_id, scope, group_id)
        r = requests.post(user_permission_url, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if group is assigned to user
        print('Check if group is assigned to user...')
        r = requests.get(base_url + ACCOUNT_USER_PERMISSION_GROUPS % (new_user_id, scope), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        groups_len = len(r.json()['results'])

        # Check if assigned group got "selected": true
        for i in range(groups_len):
            if r.json()['results'][i]['id'] == group_id:
                if not r.json()['results'][i]['selected']:
                    self.fail('Group is not assigned to user')

        # Delete user from permission group
        print('Delete user from permission group...')
        r = requests.delete(user_permission_url, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if user is deleted from permission group
        print('Check if user is deleted from permission group...')
        r = requests.get(base_url + ACCOUNT_USER_PERMISSION_GROUPS % (new_user_id, scope), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if unassigned group got "selected": false
        for i in range(groups_len):
            if r.json()['results'][i]['id'] == group_id:
                if r.json()['results'][i]['selected']:
                    self.fail('Group is not unassigned from user.')

    def test_assign_delete_permission_group_by_hub_id(self):

        marker = generate_unique()
        group_name = 'Auto API permission group %s' % marker
        permission_group_data = '{"title": "%s", "scope":"hub"}' % group_name

        # Create new permission group
        print('Create permission group...')
        r = requests.post(base_url + PERMISSION_GROUPS_LIST, data=permission_group_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['title'] != group_name or r.json()['scope'] != 'hub':
            self.fail('Wrong response.')

        group_id = r.json()['id']

        # Assign permission group to user
        print('Assign permission group to user...')
        user_permission_url = base_url + ACCOUNT_USER_PERMISSION_GROUP_RELATION % (new_user_id, hub_id, group_id)
        r = requests.post(user_permission_url, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if group is assigned to user
        print('Check if group is assigned to user...')
        r = requests.get(base_url + ACCOUNT_USER_PERMISSION_GROUPS % (new_user_id, hub_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        groups_len = len(r.json()['results'])

        # Check if assigned group got "selected": true
        for i in range(groups_len):
            if r.json()['results'][i]['id'] == group_id:
                if not r.json()['results'][i]['selected']:
                    self.fail('Group is not assigned to user.')

        # Delete user from permission group
        print('Delete user from permission group...')
        r = requests.delete(user_permission_url, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if user is deleted from permission group
        print('Check if user is deleted from permission group...')
        r = requests.get(base_url + ACCOUNT_USER_PERMISSION_GROUPS % (new_user_id, hub_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if unassigned group got "selected": false
        for i in range(groups_len):
            if r.json()['results'][i]['id'] == group_id:
                if r.json()['results'][i]['selected']:
                    self.fail('Group is not unassigned from user.')

    def test_assign_default_permissions_group_to_user_by_hub_id(self):

        # Assign default permission group to user
        print('Assign default permission group to user...')
        user_permission_url = base_url + ACCOUNT_USER_PERMISSION_GROUPS % (new_user_id, hub_id)
        r = requests.post(user_permission_url, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if group is assigned to user
        print('Check if group is assigned to user...')
        r = requests.get(base_url + ACCOUNT_USER_PERMISSION_GROUPS % (new_user_id, hub_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        groups_len = len(r.json()['results'])

        # Check if assigned group got "selected": true
        for i in range(groups_len):
            if r.json()['results'][i]['title'] == 'Stage Fan':
                if not r.json()['results'][i]['selected']:
                    self.fail('Group is not assigned to user.')

        # Delete user from default permission group
        print('Delete user from permission group...')
        r = requests.delete(user_permission_url, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if user is deleted from default permission group
        print('Check if user is deleted from permission group...')
        r = requests.get(base_url + ACCOUNT_USER_PERMISSION_GROUPS % (new_user_id, hub_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if unassigned group got "selected": false
        for i in range(groups_len):
            if r.json()['results'][i]['title'] == 'Stage Fan':
                if r.json()['results'][i]['selected']:
                    self.fail('Group is not unassigned from user.')

    def test_delete_all_user_permissions_groups_in_specified_stage(self):

        marker = generate_unique()
        group_name = 'Auto API permission group %s' % marker
        permission_group_data = '{"title": "%s", "scope":"app"}' % group_name

        # Create new permission group
        print('Create permission group...')
        r = requests.post(base_url + PERMISSION_GROUPS_LIST, data=permission_group_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['title'] != group_name or r.json()['scope'] != 'app':
            self.fail('Wrong response.')

        group_id = r.json()['id']
        scope = r.json()['scope']

        # Assign permission group to user
        print('Assign permission group to user...')
        user_permission_url = base_url + ACCOUNT_USER_PERMISSION_GROUP_RELATION % (new_user_id, scope, group_id)
        r = requests.post(user_permission_url, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if group is assigned to user
        print('Check if group is assigned to user...')
        r = requests.get(base_url + ACCOUNT_USER_PERMISSION_GROUPS % (new_user_id, scope), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        groups_len = len(r.json()['results'])

        # Check if assigned group got "selected": true
        for i in range(groups_len):
            if r.json()['results'][i]['id'] == group_id:
                if not r.json()['results'][i]['selected']:
                    self.fail('Group is not assigned to user.')

        # Delete all user permission groups
        print('Delete all user permission groups...')
        r = requests.delete(base_url + ACCOUNT_USER_PERMISSION_GROUPS % (new_user_id, scope), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if user is deleted from permission group
        print('Check if all user permission groups are deleted ...')
        r = requests.get(base_url + ACCOUNT_USER_PERMISSION_GROUPS % (new_user_id, scope), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if unassigned group got "selected": false
        for i in range(groups_len):
            if r.json()['results'][i]['id'] == group_id:
                if r.json()['results'][i]['selected']:
                    self.fail('Group is not unassigned from user.')

    @unittest.skip
    def test_sns_endpoint(self):

        # Activate SNS endpoint
        print('Activate SNS endpoint ...')
        endpoint_data = json.dumps({"device_type": "android", "token": TestData.device_token})
        url = base_url + ACCOUNT_SNS_ENDPOINT % TestData.device_id
        r = requests.post(url, data=endpoint_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Deactivate SNS endpoint
        print('Deactivate SNS endpoint ...')
        r = requests.delete(base_url + ACCOUNT_SNS_ENDPOINT % TestData.device_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

    @unittest.skip
    def test_send_push_notification(self):

        marker = generate_unique()
        payload = json.dumps({"message": "Test Push %s" % marker})

        # Send push notification
        print('Send push notification ...')
        r = requests.post(base_url + ACCOUNT_PUSH % new_user_id, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if 'Sent to' not in r.text:
            self.fail('Wrong response.')

    def test_resend_verification_email(self):

        # Resend verification email
        print('Resend verification email...')
        r = requests.get(base_url + ACCOUNT_RESEND_VERIFICATION_EMAIL, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

    def test_connect_fb_account(self):

        # Create new facebook user
        print("Create new Facebook user...")
        url = 'https://graph.facebook.com/v2.5/%s/accounts/test-users?access_token=%s'
        r = requests.post(url % (TestData.facebook_app_id, TestData.access_token))
        print('Status code - %s' % r.status_code, '\n')

        fb_id = r.json()["id"]
        fb_access_token = r.json()["access_token"]

        # Connect FB account
        print('Connect FB account...')
        fb_data = json.dumps({"fb_token": fb_access_token})
        r = requests.post(base_url + ACCOUNT_CONNECT_FACEBOOK, data=fb_data, headers=new_user_headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Verify FB connect to user account
        print('Verify FB account...')
        r = requests.get(base_url + ACCOUNT_USER, headers=new_user_headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['facebook_id'] != fb_id:
            self.fail('FB account not connect')

    def test_loyalty_level_up(self):

        # Subscribe to hub as new user
        print('Subscribe to hub as new user...')
        r = requests.post(base_url + ACCOUNT_SUBSCRIBE_HUB % hub_id, headers=new_user_headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Set 'Front Row' loyalty level
        print('Set "Front Row" user loyalty level...')
        r = requests.post(base_url + ACCOUNT_LOYALTY_LEVEL % (new_user_id, hub_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['loyalty_level']['value'] != 3 or r.json()['loyalty_level']['title'] != 'Front Row':
            self.fail('Wrong response.')

        # Set 'VIP' loyalty level
        print('Set "VIP" user loyalty level...')
        r = requests.post(base_url + ACCOUNT_LOYALTY_LEVEL % (new_user_id, hub_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['loyalty_level']['value'] != 2 or r.json()['loyalty_level']['title'] != 'VIP':
            self.fail('Wrong response.')

        # Set 'All Access' loyalty level
        print('Set "All Access" user loyalty level...')
        r = requests.post(base_url + ACCOUNT_LOYALTY_LEVEL % (new_user_id, hub_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['loyalty_level']['value'] != 1 or r.json()['loyalty_level']['title'] != 'All Access':
            self.fail('Wrong response.')

        # Set 'Bkstg' loyalty level
        print('Set "Bkstg" user loyalty level...')
        r = requests.post(base_url + ACCOUNT_LOYALTY_LEVEL % (new_user_id, hub_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['loyalty_level']['value'] != 0 or r.json()['loyalty_level']['title'] != 'Bkstg':
            self.fail('Wrong response.')

    @unittest.skip
    def test_ban_unban_user(self):  # skipped as functionality is not relevant at the moment

        # Subscribe to hub
        print('Subscribe to hub ...')
        r = requests.post(base_url + ACCOUNT_SUBSCRIBE_HUB % hub_id, headers=new_user_headers_4)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Ban user
        print('Ban user...')
        r = requests.post(base_url + ACCOUNT_BAN % new_user_id_4, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if user is banned
        print('Check if uer is banned...')
        r = requests.get(base_url + ACCOUNT_PROFILE_BY_ADMIN % (new_user_id_4, hub_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['is_banned'] == True:
            self.fail('Wrong response')

        # Unban user
        print('Unbanned user...')
        r = requests.delete(base_url + ACCOUNT_BAN % new_user_id_4, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if user is unbanned
        print('Check if uer is unbanned...')
        r = requests.get(base_url + ACCOUNT_PROFILE_BY_ADMIN % (new_user_id_4, hub_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['is_banned'] == False:
            self.fail('Wrong response')

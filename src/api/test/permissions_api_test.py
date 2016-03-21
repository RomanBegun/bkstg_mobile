import json
import logging
import unittest
import requests

from src.api.helpers.unique_gen import *
from src.api.setup.preconditions import Preconditions
from src.api.urls.api_urls import *


class PermissionsApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        global auth, base_url, headers

        auth = Preconditions()
        auth.log_in()
        base_url = auth.env.base_url
        headers = {"Authorization": "Token %s" % auth.token}

        global permission_group_id

        auth.create_permission_group()
        permission_group_id = auth.permission_group_id

    @classmethod
    def tearDownClass(cls):

        print('Delete permission group...')
        r = requests.delete(base_url + PERMISSION_GROUP % permission_group_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        if '20' not in str(r.status_code):
            raise AssertionError(r.status_code)

    def test_create_permissions_group(self):

        marker = generate_unique()
        group_name = 'Auto API permission group %s' % marker
        permission_group_data = '{"title": "%s", "scope":"app"}' % group_name

        # Create permission group
        print('Create permission group...')
        r = requests.post(base_url + PERMISSION_GROUPS_LIST, data=permission_group_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['title'] != group_name or r.json()['scope'] != 'app':
            self.fail('Wrong response.')
            
        new_group_id = r.json()['id']

        print('Delete permission group...')
        r = requests.delete(base_url + PERMISSION_GROUP % new_group_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

    def test_get_permissions_groups_list(self):

        # Get permission groups list
        print('Get permission groups list...')
        r = requests.get(base_url + PERMISSION_GROUPS_LIST + '?limit=100', headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        group_list_dict = json.loads(json.dumps(r.json()))
        id_count = len(list(filter(lambda i: bool(i.get('id')), group_list_dict['results'])))
        if id_count <= 2 or not r.json()['results'][0]['title']:
            self.fail('Wrong response.')

    def test_get_permissions_group(self):

        # Get permission group
        print('Get permission group...')
        r = requests.get(base_url + PERMISSION_GROUP % permission_group_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['id'] != permission_group_id or 'Auto API' not in r.json()['title']:
            self.fail('Wrong response.')

    def test_get_group_permissions(self):

        # Get group permissions
        print('Get group permissions...')
        r = requests.get(base_url + PERMISSION_GROUP_PERMISSIONS_LIST % permission_group_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        permissions_len = len(r.json()['results'])
        self.permission = ''
        for i in range(permissions_len):
            if 'community:post:edit' in r.json()['results'][i]:
                self.permission = r.json()['results'][i]
        if 'community:post:edit' not in self.permission:
            self.fail('Wrong response.')

    def test_edit_permissions_group(self):

        marker = generate_unique()
        edited_group_name = 'Edited Auto API permission group %s' % marker
        permission_group_data = '{"title": "%s", "scope":"hub"}' % edited_group_name

        # Edit permission group
        print('Edit permission group...')
        url = base_url + PERMISSION_GROUPS_LIST + '/%s' % permission_group_id
        r = requests.put(url, data=permission_group_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['title'] != edited_group_name or r.json()['scope'] != 'hub':
            self.fail('Wrong response.')

    def test_delete_permissions_group(self):

        # Precondition
        auth.create_permission_group()
        permission_group_id_2 = auth.permission_group_id

        # Delete permission group
        print('Delete permission group...')
        r = requests.delete(base_url + PERMISSION_GROUP % permission_group_id_2, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check id permission group is deleted
        print('Check id permission group is deleted...')
        r = requests.get(base_url + PERMISSION_GROUPS_LIST, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        groups_len = len(r.json()['results'])
        for i in range(groups_len):
            if r.json()['results'][i]['id'] == permission_group_id_2:
                self.fail('Wrong response.')

    def test_add_remove_group_permission(self):

        # Add permission to group
        print('Assign permission to group...')
        permission = 'feed:post:edit'
        url = base_url + PERMISSION_GROUP_SET_PERMISSION % (permission_group_id, permission)
        r = requests.post(url, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if permission is added
        print('Check if permission is added...')
        r = requests.get(base_url + PERMISSION_GROUP_PERMISSIONS_LIST % permission_group_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        permissions_len = len(r.json()['results'])
        for i in range(permissions_len):
            if r.json()['results'][i][0] == permission:
                if r.json()['results'][i][1]['active'] is not True:
                    self.fail('%s permission is not active.' % permission)

        # Remove permission from group
        print('Delete permission from group...')
        r = requests.delete(base_url + PERMISSION_GROUP_SET_PERMISSION % (permission_group_id, permission), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if permission is deleted
        print('Check if permission is deleted...')
        r = requests.get(base_url + PERMISSION_GROUP_PERMISSIONS_LIST % permission_group_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        permissions_len = len(r.json()['results'])
        for i in range(permissions_len):
            if r.json()['results'][i][0] == permission:
                if r.json()['results'][i][1]['active'] is True:
                    self.fail('%s permission is still active.' % permission)

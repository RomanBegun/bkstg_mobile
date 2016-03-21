import json
import unittest
import requests
import logging

from src.api.helpers.unique_gen import *
from src.api.setup.test_data import TestData
from src.api.urls.api_urls import *
from src.api.setup.preconditions import Preconditions


class HubsApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        global auth, headers, base_url, user_id, hub_id

        auth = Preconditions()
        base_url = auth.env.base_url

        auth.log_in()
        headers = {"Authorization": "Token %s" % auth.token, "BKSTG_DISABLE_CACHE": "True"}
        user_id = auth.user_id

        auth.create_hub(headers)
        hub_id = auth.hub_id

        global new_user_id, celebrity_headers

        auth.create_user()        
        new_user_id = auth.new_user_id
        celebrity_headers = {"Authorization": "Token %s" % auth.new_user_token, "BKSTG_DISABLE_CACHE": "True"}

        global new_user_id_2, new_user_headers_2, new_user_id_3, new_user_headers_3
        
        auth.create_user()
        new_user_id_2 = auth.new_user_id
        new_user_headers_2 = {"Authorization": "Token %s" % auth.new_user_token, "BKSTG_DISABLE_CACHE": "True"}

        auth.create_user()
        new_user_id_3 = auth.new_user_id
        new_user_headers_3 = {"Authorization": "Token %s" % auth.new_user_token, "BKSTG_DISABLE_CACHE": "True"}

        global image_id, image_item
        
        auth.upload_image(TestData.image_path)
        image_item = auth.image_item
        image_id = auth.image_id

    @classmethod
    def tearDownClass(cls):

        # Delete hub
        print('Delete hub...')
        r = requests.delete(base_url + HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        if '20' not in str(r.status_code):
            raise AssertionError(r.status_code)

    def test_get_hubs_list(self):

        # Get hubs
        print('Get hubs list...')
        r = requests.get(base_url + HUBS_LIST, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['results'][0]['available_sections'] or not r.json()['results'][0]['id']:
            self.fail('Error')

    def test_get_hubs_list_for_admin(self):

        # Get admin hubs
        print('Get admin hubs list...')
        r = requests.get(base_url + ADMIN_HUBS_LIST, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['results'][0]['id']:
            self.fail('Wrong response.')

    def test_get_hub(self):

        # Get hub posts
        print('Get hub...')
        r = requests.get(base_url + HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['id'] != hub_id or 'Test Hub' not in r.json()['name']:
            self.fail('Wrong response.')

    def test_create_delete_hub(self):

        marker = generate_unique()
        raw = {
                "description": "Test active hub.",
                "is_deleted": "false",
                "is_private": "false",
                "main_color": "#d8f3c9",
                "name": "Test Hub %s" % marker,
                "secondary_color": "#ffffff"
        }
        payload = json.dumps(raw)

        # Create hub
        print('Create hub...')
        r = requests.post(base_url + HUBS_LIST, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['name'] == "Test Hub %s" % marker:
            self.fail('Wrong response.')

        test_hub_id = r.json()['id']

        # Delete hub
        print('Delete hub...')
        r = requests.delete(base_url + HUB % test_hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        print('Check if hub is removed...')
        r = requests.get(base_url + ADMIN_HUBS_LIST, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        hubs_amount = len(r.json()['results'])
        for i in range(hubs_amount):
            if r.json()['results'][i]['id'] == test_hub_id:
                self.fail('Wrong response.')

    @unittest.skip
    def test_edit_hub(self):

        marker = generate_unique()
        hub_payload = '{"name": "Test Hub %s", "main_color": "#fffffa"}' % marker

        # Edit hub
        print('Edit hub...')
        r = requests.put(base_url + EDIT_HUB % hub_id, data=hub_payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        # if not r.json()['name'] == 'Test Hub %s' % marker:
        #     self.fail('Wrong response.')

        # Check if hub is edited
        print('Get hub data to check if hub is edited...')
        r = requests.get(base_url + HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['name'] == 'Test Hub %s' % marker:
            self.fail('Wrong response.')

    def test_create_ghost_hub(self):

        marker = generate_unique()
        ghost_payload = '{"name": "Ghost Test Hub %s"}' % marker

        # Create ghost hub
        print('Create ghost hub...')
        r = requests.post(base_url + GHOST_HUB, data=ghost_payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['name'] == "Ghost Test Hub %s" % marker:
            self.fail('Wrong response.')

    def test_get_hub_settings(self):

        # Get hub settings
        print('Get hub settings...')
        r = requests.get(base_url + HUB_SETTINGS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['form']:
            self.fail('Wrong response.')

    @unittest.skip
    def test_edit_hub_settings(self):

        marker = generate_unique()
        payload = '{"community:community_title": "Test Community %s"}' % marker

        # Edit hub settings
        print('Edit hub settings...')
        r = requests.put(base_url + HUB_SETTINGS % hub_id, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['settings']['community']['community_title'] != "Test Community %s" % marker:
            self.fail('Wrong response.')

    @unittest.skip  # skipped as not relevant
    def test_sign_unsign_hub_user(self):

        # Get permission groups list
        print('Get permission groups list...')
        r = requests.get(base_url + PERMISSION_GROUPS_LIST + '?limit=100', headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        group_list_dict = json.loads(json.dumps(r.json()))
        id_count = len(list(filter(lambda i: bool(i.get('id')), group_list_dict['results'])))
        if id_count <= 2 or not r.json()['results'][0]['title']:
            self.fail('Wrong response.')

        # Get Stage Admin permission group id
        for i in range(id_count):
            if r.json()['results'][i]['title'] == 'Admin':
                self.admin_group_id = r.json()['results'][i]['id']
                continue

        # Assign Stage Admin permission group to user
        print('Assign Stage Admin permission group to user...')
        permission_url = base_url + ACCOUNT_USER_PERMISSION_GROUP_RELATION % (new_user_id, hub_id, self.admin_group_id)
        r = requests.post(permission_url, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Adding hub signature as Stage Admin
        print('Add signature to hub as Stage Admin...')
        hub_payload = json.dumps({"signature_image": image_item})
        r = requests.put(base_url + EDIT_HUB % hub_id, data=hub_payload, headers=celebrity_headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['signature_image']['id'] != image_item['id']:
            self.fail('Signature is not saved')

        # Subscribe to hub as new user
        print('Subscribe to hub as new user...')
        r = requests.post(base_url + ACCOUNT_SUBSCRIBE_HUB % hub_id, headers=new_user_headers_2)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Sign hub as Stage Admin to new user
        print('Sign new user hub as Stage Admin...')
        r = requests.post(base_url + HUB_SIGN_HUB % (hub_id, new_user_id_2), headers=celebrity_headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['id'] != image_id:
            self.fail('Wrong response.')

        # Unsign user hub
        print('Unsign user hub as Stage Admin...')
        r = requests.delete(base_url + HUB_SIGN_HUB % (hub_id, new_user_id_2), headers=celebrity_headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

    @unittest.skip  # not relevant at the moment
    def test_add_hub_signature(self):

        payload = json.dumps({"signature_image": image_item})

        # Add hub signature
        print('Add hub signature...')
        r = requests.put(base_url + EDIT_HUB % hub_id, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['signature_image']['id'] != image_item['id']:
            self.fail('Signature is not saved.')

        # Get hub
        print('Check if signature is added...')
        r = requests.get(base_url + HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['signature_image']['id'] != image_item['id']:
            self.fail('Signature is not saved.')

    def test_get_hub_team(self):

        # Get hub team
        print('Get new hub team...')
        r = requests.get(base_url + HUB_TEAM % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        team_len = len(r.json()['results'])

        # Check if team member id (John Brown) is in list
        for i in range(team_len):
            if r.json()['results'][i]['id'] == user_id:
                self.team_member_id = user_id
        if self.team_member_id != user_id:
            self.fail('Wrong response.')

    def test_get_hub_team_aliases(self):

        # Get hub team aliases
        print('Get new hub aliases...')
        r = requests.get(base_url + HUB_TEAM_ALIASES % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        alias_len = len(r.json()['results'])

        # Check if team member id (John Brown) is in aliases list
        for i in range(alias_len):
            if r.json()['results'][i]['alias']['id'] == user_id:
                self.alias_id = user_id
        if self.alias_id != user_id:
            self.fail('Wrong response.')

    def test_create_delete_hub_team_alias(self):

        # Alias must be in stage team

        # Assign new user as artist for current stage
        # Get permission groups list
        print('Get permission groups list...')
        r = requests.get(base_url + PERMISSION_GROUPS_LIST + '?limit=100', headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        groups_len = len(r.json()['results'])
        for i in range(groups_len):
            if r.json()['results'][i]['title'] == 'Artist':
                self.group_id = r.json()['results'][i]['id']

        # Assign permission group to user
        print('Set Artist permission group to new user in current stage...')
        user_permission_url = base_url + ACCOUNT_USER_PERMISSION_GROUP_RELATION % (new_user_id, hub_id, self.group_id)
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
            if r.json()['results'][i]['id'] == self.group_id:
                if not r.json()['results'][i]['selected']:
                    self.fail('Group is not assigned to user.')

        # Create alias
        print('Create stage team alias...')
        r = requests.post(base_url + HUB_TEAM_ALIAS % (hub_id, new_user_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['alias']['id'] != new_user_id:
            self.fail('Alias is not assigned to user.')

        # Delete alias
        print('Delete alias from stage team...')
        r = requests.delete(base_url + HUB_TEAM_ALIAS % (hub_id, new_user_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if user alias is deleted
        print('Check if user alias is deleted...')
        r = requests.get(base_url + HUB_TEAM_ALIASES % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        alias_len = len(r.json()['results'])
        # Check if new team member is removed from aliases list
        self.alias_id = ''
        for i in range(alias_len):
            if r.json()['results'][i]['alias']['id'] == new_user_id:
                self.fail('Wrong response.')

    def test_get_hub_team_alias(self):

        # Get John Brown alias(added in create_hub() precondition)
        print('Get alias...')
        r = requests.get(base_url + HUB_TEAM_ALIAS % (hub_id, user_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['alias']['id'] != user_id:
            self.fail('Wrong response.')

    def test_link_unlink_hub_team_alias(self):

        # User must be in stage team in order to have ability to link to alias
        # Assign new user as artist for current stage

        # Get permission groups list
        print('Get permission groups list...')
        r = requests.get(base_url + PERMISSION_GROUPS_LIST + '?limit=100', headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        groups_len = len(r.json()['results'])
        for i in range(groups_len):
            if r.json()['results'][i]['title'] == 'Artist':
                self.group_id = r.json()['results'][i]['id']

        # Assign permission group to user
        print('Set Artist permission group to new user in current stage...')
        user_permission_url = base_url + ACCOUNT_USER_PERMISSION_GROUP_RELATION % (new_user_id, hub_id, self.group_id)
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
            if r.json()['results'][i]['id'] == self.group_id:
                if not r.json()['results'][i]['selected']:
                    self.fail('Group is not assigned to user.')

        # Link new user to John Brown alias (added in create_hub() precondition)
        print('Link new user to alias...')
        r = requests.post(base_url + HUB_TEAM_LINK_ALIAS % (hub_id, user_id, new_user_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['alias']['id'] != user_id:
            self.fail('User is not linked to alias.')

        # Check if new user is linked to John Brown alias
        print('Check if user is linked to alias...')
        r = requests.get(base_url + HUB_TEAM_ALIAS % (hub_id, user_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['users'][0]['id'] != new_user_id:
            self.fail('Wrong response.')

        # Unlink new user from John Brown alias
        print('Unlink new user from alias')
        r = requests.delete(base_url + HUB_TEAM_LINK_ALIAS % (hub_id, user_id, new_user_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if new user is unlinked from John Brown alias
        print('Check if user is unlinked from alias...')
        r = requests.get(base_url + HUB_TEAM_ALIAS % (hub_id, user_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['users']:
            self.fail('Wrong response.')

    @unittest.skip
    def test_assign_artist_group_to_user(self):

        # Get permission groups list
        print('Get permission groups list...')
        r = requests.get(base_url + PERMISSION_GROUPS_LIST + '?limit=100', headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        groups_len = len(r.json()['results'])
        for i in range(groups_len):
            if r.json()['results'][i]['title'] == 'Artist':
                self.group_id = r.json()['results'][i]['id']

        # Assign permission group to user
        print('Set Artist permission group to new user in current stage...')
        user_permission_url = base_url + ACCOUNT_USER_PERMISSION_GROUP_RELATION % (new_user_id, hub_id, self.group_id)
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
            if r.json()['results'][i]['id'] == self.group_id:
                if not r.json()['results'][i]['selected']:
                    self.fail('Group is not assigned to user.')

        # Check if user is Artist
        print('Check if user appears as Artist in get hub request...')
        r = requests.get(base_url + HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        celebrities_len = len(r.json()['celebrities'])
        self.new_artist_id = ''
        for i in range(celebrities_len):
            if r.json()['celebrities'][i]['id'] == new_user_id:
                self.new_artist_id = new_user_id
        if self.new_artist_id != new_user_id:
            self.fail('New Artist is not present in stage celebrities.')

    @unittest.skip
    def test_search_hub_users(self):

        # Subscribe to hub as new user
        print('Subscribing to hub as new user...')
        r = requests.post(base_url + ACCOUNT_SUBSCRIBE_HUB % hub_id, headers=new_user_headers_3)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Search hub users
        print('Search hub users...')
        r = requests.get(base_url + HUB_SEARCH % hub_id, headers=headers)
        results_len = len(r.json()['results'])
        self.searched_user_id = ''
        for i in range(results_len):
            if r.json()['results'][i]['id'] == new_user_id_3:
                self.searched_user_id = new_user_id_3
        if self.searched_user_id != new_user_id_3:
            self.fail('Wrong response')

    def test_get_hub_for_admin(self):

        # Get hub for admin
        print('Get hub for admin...')
        r = requests.get(base_url + HUB_ADMIN % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['id'] != hub_id:
            self.fail('Wrong response')

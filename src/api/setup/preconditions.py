import json
import logging
import unittest
import requests

from src.api.helpers.unique_gen import *
from src.api.urls.api_urls import *
from src.api.setup.environment import TestEnvironment
from src.api.setup.test_data import TestData
from src.api.helpers.upload_to_sandbox import Upload


class Preconditions(unittest.TestCase):

    def __init__(self):
        super().__init__()
        self.env = TestEnvironment()
        self.env.set_env_from_arg()
        self.base_url = self.env.base_url

    def log_in(self):

        login_payload = '{"email": "%s", "password": "%s"}' % (TestData.email, TestData.password)

        # Log in
        print('Log in...')
        r = requests.post(self.base_url + AUTH_LOGIN, data=login_payload)
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        print('Status code - %s' % r.status_code, '\n')
        if not r.json()['token']:
            self.fail('User is not logged in.')

        self.token = r.json()['token']

        print('Get user data...')
        r = requests.get(self.base_url + ACCOUNT_USER, headers={"Authorization": 'Token %s' % self.token})
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['username'] != 'admin':
            self.fail('Wrong response.')

        self.user_id = r.json()['id']
        self.user_name = r.json()['username']
        self.user_email = r.json()['email']

    def log_in_as_celebrity(self):

        payload = '{"email": "%s", "password": "%s"}' % (TestData.celebrity_email, TestData.celebrity_password)

        # Log in as celebrity
        print('Log in as celebrity...')
        r = requests.post(self.base_url + AUTH_LOGIN, data=payload)
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        print('Status code - %s' % r.status_code, '\n')
        if not r.json()['token']:
            self.fail('User is not logged in.')

        self.celebrity_token = r.json()['token']

    def create_user(self):

        marker = generate_unique()

        signup_data = {"username": "test-%s" % marker,
                       "password": "12345678",
                       "email": "bkstg.test-API%s@stub.bkstg.com" % marker,
                       "device_type": "ios",
                       "device_id": "4B8F7BDD-8D8D-40A2-9412-8A5ECD5BF1A3",
                       "birthday": "1991-08-08",
                       "full_name": "API Test %s" % marker
                       }
        payload = json.dumps(signup_data)

        # Register user
        print('Register user...')
        r = requests.post(self.base_url + AUTH_SIGN_UP, data=payload)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['token']:
            self.fail('User is not registered properly.')

        self.new_user_token = r.json()['token']

        print('Check user data...')
        r = requests.get(self.base_url + ACCOUNT_USER, headers={"Authorization": 'Token %s' % self.new_user_token})
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['username'] != 'test-%s' % marker or r.json()['birthday'] != '1991-08-08':
            self.fail('User is not registered properly')

        self.new_user_id = r.json()['id']
        self.new_user_name = r.json()['username']
        self.new_user_email = r.json()['email']

    def create_hub(self, headers):

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
        r = requests.post(self.base_url + HUBS_LIST, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['name'] == "Test Hub %s" % marker:
            self.fail('Failed to create hub.')

        self.hub_id = r.json()['id']
        print('Hub ID: %s' % self.hub_id)
        print('Hub name: Test Hub %s\n' % marker)

        ''' Assign Admin(John Brown) as artist manager for current stage '''

        # Get permission groups list
        print('Get permission groups list...')
        r = requests.get(self.base_url + PERMISSION_GROUPS_LIST + '?limit=100', headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        groups_len = len(r.json()['results'])
        for i in range(groups_len):
            if r.json()['results'][i]['title'] == 'Management':
                self.group_id = r.json()['results'][i]['id']

        # Assign permission group to user
        print('Set Artist Manager permission group to John Brown in current stage...')
        user_permission_url = self.base_url + ACCOUNT_USER_PERMISSION_GROUP_RELATION
        r = requests.post(user_permission_url % (self.user_id, self.hub_id, self.group_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if group is assigned to user
        print('Check if group is assigned to user...')
        r = requests.get(self.base_url + ACCOUNT_USER_PERMISSION_GROUPS % (self.user_id, self.hub_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if assigned group got "selected": true
        groups_len = len(r.json()['results'])
        for i in range(groups_len):
            if r.json()['results'][i]['id'] == self.group_id:
                if not r.json()['results'][i]['selected']:
                    self.fail('Group is not assigned to user.')

        # Assign alias for John Brown in current stage
        print('Assign alias for John Brown in current stage...')
        r = requests.post(self.base_url + HUB_TEAM_ALIAS % (self.hub_id, self.user_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['alias']['id'] != self.user_id:
            self.fail('Alias is not assigned.')

    def delete_hub(self, headers, hub_id):

        # Delete hub
        print('Delete hub...')
        r = requests.delete(self.base_url + HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

    def create_community_post(self, headers, hub_id):

        marker = generate_unique()

        post_data = {"post_type": "text", "text": "API auto community post - %s" % marker, "lan": 45.45, "lat": 24.23}
        payload = json.dumps(post_data)

        # Create community post
        print('Create community post...')
        url = self.base_url + COMMUNITY_HUB_POSTS % hub_id
        r = requests.post(url, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['text'] == 'API auto community post - %s' % marker:
            self.fail('Failed to create community post.')

        self.community_post_id = r.json()['id']
        self.short_url = r.json()['short_url']

    def create_community_post_comment(self, headers, hub_id, post_id):

        marker = generate_unique()
        comment = 'Auto API community comment - %s' % marker
        comment_data = '{"text" : "%s"}' % comment

        # Post community comment
        print('Create community post comment...')
        url = self.base_url + COMMUNITY_HUB_POST_COMMENTS % (hub_id, post_id)
        r = requests.post(url, data=comment_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['text'] == comment:
            self.fail('Failed to post comment.')

        self.community_post_comment_id = r.json()['id']

    def create_feed_post(self, headers, hub_id):

        marker = generate_unique()
        post_data = {"post_type": "text", "text": "API auto feed post - %s!" % marker, "is_private": False}
        post_json_data = json.dumps(post_data)

        # Create feed post
        print('Create feed post...')
        url = self.base_url + FEED_POSTS_LIST % hub_id
        r = requests.post(url, data=post_json_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['text'] == "API auto feed post - %s!" % marker or r.json()['is_private']:
            self.fail('Failed to create feed post.')

        self.feed_post_id = r.json()['id']
        self.short_url = r.json()['short_url']

        post_status = 'live'

        # Switch post status to 'live'
        print('Set post status to "%s"...' % post_status)
        url = self.base_url + FEED_SWITCH_POST % (self.hub_id, self.feed_post_id, post_status)
        r = requests.post(url, headers={"Authorization": 'Token %s' % self.token})
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if feed post status switched to "live"
        print('Check if feed post status switched to "live"...')
        r = requests.get(self.base_url + FEED_POST % (hub_id, self.feed_post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        if not r.json()['post_status'] == post_status:
            self.fail('Failed to switch post status to "live".')

    def create_feed_post_comment(self, headers, hub_id, post_id):

        marker = generate_unique()
        comment = 'API auto feed comment - %s' % marker
        comment_payload = '{"text": "%s"}' % comment

        # Create feed post comment
        print('Create comment for feed post...')
        url = self.base_url + FEED_POST_COMMENTS_LIST % (hub_id, post_id)
        r = requests.post(url, data=comment_payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['text'] == comment:
            self.fail('Failed to create feed post comment.')

        self.feed_post_comment_id = r.json()['id']

    def create_permission_group(self):

        marker = generate_unique()
        group_name = 'Auto API permission group %s' % marker
        permission_group_data = '{"title": "%s", "scope":"app"}' % group_name

        # Create permission group
        print('Create permission group...')
        url = self.base_url + PERMISSION_GROUPS_LIST
        r = requests.post(url, data=permission_group_data, headers={"Authorization": 'Token %s' % self.token})
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['title'] != group_name or r.json()['scope'] != 'app':
            self.fail('Failed to create permission group.')

        self.permission_group_id = r.json()['id']

    def upload_image(self, image_path):

        self.image_key = Upload.upload_to_sandbox(image_path)

        file_data = {"key": "%s" % self.image_key,
                       "title": "background",
                       "mime_type": "image/jpeg",
                       "width": 1500,
                       "height": 1000
                       }
        payload = json.dumps(file_data)

        # After upload
        print('After upload...')
        url = self.base_url + MEDIA_AFTER_UPLOAD
        r = requests.post(url, data=payload, headers={"Authorization": 'Token %s' % self.token})
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['item']['content_type'] != 'image' or r.json()['item']['title'] != 'background':
            self.fail('Wrong response.')

        self.image_id = r.json()['item']['id']
        self.image_item = r.json()['item']

    def upload_video(self, video_path):

        self.video_key = Upload.upload_to_sandbox(video_path)

        file_title = 'Should’ve Been Us (Official)'
        file_data = {"key": "%s" % self.video_key,
                       "title": "%s" % file_title,
                       "mime_type": "video/mp4",
                       "width": 720,
                       "height": 406
                       }
        payload = json.dumps(file_data)

        # After upload
        print('After upload...')
        url = self.base_url + MEDIA_AFTER_UPLOAD
        r = requests.post(url, data=payload, headers={"Authorization": 'Token %s' % self.token})
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['item']['content_type'] != 'native_video' or r.json()['item']['title'] != file_title:
            self.fail('Wrong response')

        self.video_id = r.json()['item']['id']
        self.video_item = r.json()['item']

    def upload_audio(self, audio_path):

        self.audio_key = Upload.upload_to_sandbox(audio_path)

        file_title = "Mother's Journey"
        file_data = {"key": "%s" % self.audio_key,
                        "title": "%s" % file_title,
                        "mime_type": "audio/mpeg3",
                        "width": 0,
                        "height": 0
                       }
        payload = json.dumps(file_data)

        # After upload
        print('After upload...')
        url = self.base_url + MEDIA_AFTER_UPLOAD
        r = requests.post(url, data=payload, headers={"Authorization": 'Token %s' % self.token})
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['item']['content_type'] != 'native_audio' or r.json()['item']['title'] != file_title:
            self.fail('Wrong response')

        self.audio_id = r.json()['item']['id']
        self.audio_item = r.json()['item']

    def upload_thumbnail(self, thumbnail_path):

        self.thumbnail_key = Upload.upload_to_sandbox(thumbnail_path)

        file_data = {"key": "%s" % self.thumbnail_key,
                       "title": "10",
                       "mime_type": "image/jpeg",
                       "width": 720,
                       "height": 406
                       }
        payload = json.dumps(file_data)

        # After upload
        print('After upload...')
        url = self.base_url + MEDIA_AFTER_UPLOAD
        r = requests.post(url, data=payload, headers={"Authorization": 'Token %s' % self.token})
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['item']['content_type'] != 'image':
            self.fail('Wrong response.')

        self.thumbnail_id = r.json()['item']['id']

    def add_community_inappropriate_post(self, hub_id, word):

        marker = generate_unique()
        post_data = {"post_type": "text", "text": "API auto community inappropriate post - %s - %s" % (marker, word),
                     "lan": 45.45, "lat": 24.23}

        post_json_data = json.dumps(post_data)

        # Create community post
        print('Create community post...')
        url = self.base_url + COMMUNITY_HUB_POSTS % hub_id
        r = requests.post(url, data=post_json_data, headers={"Authorization": 'Token %s' % self.token})
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['text'] == 'API auto community inappropriate post - %s - %s' % (marker, word):
            self.fail('Failed to create community post.')

        self.inappropriate_community_post_id = r.json()['id']

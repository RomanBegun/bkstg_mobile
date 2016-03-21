import json
import logging
import requests
import unittest

from time import sleep

from src.api.helpers.unique_gen import *
from src.api.setup.preconditions import Preconditions
from src.api.urls.api_urls import *


class CommunityApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        global auth, base_url, user_name, headers, user_id

        auth = Preconditions()
        base_url = auth.env.base_url

        auth.log_in()
        user_id = auth.user_id
        user_name = auth.user_name
        headers = {"Authorization": "Token %s" % auth.token, "BKSTG_DISABLE_CACHE": "True"}
        
        global hub_id, post_id, comment_id

        auth.create_hub(headers)
        hub_id = auth.hub_id

        auth.create_community_post(headers, hub_id)
        post_id = auth.community_post_id

        auth.create_community_post_comment(headers, hub_id, post_id)
        comment_id = auth.community_post_comment_id
        
        global new_user_id, new_user_name, new_user_email, new_user_headers

        auth.create_user()
        new_user_id = auth.new_user_id
        new_user_name = auth.new_user_name
        new_user_email = auth.new_user_email
        new_user_headers = {"Authorization": "Token %s" % auth.token}

    @classmethod
    def tearDownClass(cls):

        # Delete hub
        print('Delete hub...')
        r = requests.delete(base_url + HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        if '20' not in str(r.status_code):
            raise AssertionError(r.status_code)

    def test_create_community_post(self):
        
        marker = generate_unique()
        post_data = '{"post_type" : "text", "text" : "API auto post - %s",  "lan": 45.45, "lat": 24.23}' % marker

        # Create community post
        print('Create community post...')
        r = requests.post(base_url + COMMUNITY_HUB_POSTS % hub_id, data=post_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['text'] == 'API auto post - %s' % marker:
            self.fail('Wrong response.')

    def test_edit_community_post(self):
        
        marker = generate_unique()
        post_data = {"post_type": "text", "text": "Edited API auto post - %s" % marker}
        payload = json.dumps(post_data)

        # Edit community post
        print('Edit community post...')
        r = requests.put(base_url + COMMUNITY_HUB_POST % (hub_id, post_id), data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['text'] == 'Edited API auto post - %s' % marker:
            self.fail('Wrong response.')

    def test_get_community_post(self):

        # Get community post
        print('Get community post...')
        r = requests.get(base_url + COMMUNITY_HUB_POST % (hub_id, post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['author']['id'] != user_id or r.json()['id'] != post_id or r.json()['hub_id'] != hub_id:
            self.fail('Wrong response.')

    def test_delete_community_post(self):

        marker = generate_unique()
        post_data = '{"post_type" : "text", "text" : "API auto post - %s"}' % marker

        print('Create community post...')
        r = requests.post(base_url + COMMUNITY_HUB_POSTS % hub_id, data=post_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        new_post_id = r.json()['id']

        # Delete community post
        print('Remove community post...')
        r = requests.delete(base_url + COMMUNITY_HUB_POST % (hub_id, new_post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

    def test_mark_inappropriate_community_post(self):

        marker = generate_unique()
        post_data = '{"post_type" : "text", "text" : "API auto post - %s"}' % marker

        print('Create community post...')
        r = requests.post(base_url + COMMUNITY_HUB_POSTS % hub_id, data=post_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        new_post_id = r.json()['id']

        # Mark community post as inappropriate
        print('Mark community post as inappropriate...')
        r = requests.post(base_url + COMMUNITY_HUB_INAPPROPRIATE_POST % (hub_id, new_post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if "Thank you for flagging inappropriate" not in r.json()['message']:
            self.fail('Wrong response.')

    def test_get_hub_community_posts(self):

        # Get community posts for hub
        print('Get community posts for hub...')
        r = requests.get(base_url + COMMUNITY_HUB_POSTS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['results'][0]['author']:
            self.fail('Wrong response.')

    def test_get_community_posts_by_user_id(self):

        marker = generate_unique()
        post_data = '{"post_type" : "text", "text" : "API auto post - %s",  "lan": 45.45, "lat": 24.23}' % marker

        print('Create community post...')
        r = requests.post(base_url + COMMUNITY_HUB_POSTS % hub_id, data=post_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['text'] == 'API auto post - %s' % marker:
            self.fail('Wrong response.')

        # Get community posts by user id
        print('Get community posts by user id...')
        r = requests.get(base_url + COMMUNITY_USER_POSTS % user_id, headers=new_user_headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        text = r.json()['results'][0]['text']
        if text != 'API auto post - %s' % marker:  # check if new post is the first in the list
            self.fail('Wrong response.')

    def test_like_unlike_community_post(self):

        marker = generate_unique()
        post_data = '{"post_type" : "text", "text" : "API auto post - %s"}' % marker

        print('Create community post...')
        r = requests.post(base_url + COMMUNITY_HUB_POSTS % hub_id, data=post_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        new_post_id = r.json()['id']

        # Like community post
        print('Like post...')
        r = requests.post(base_url + COMMUNITY_HUB_LIKE_POST % (hub_id, new_post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Unlike community post
        print('Unlike post...')
        r = requests.delete(base_url + COMMUNITY_HUB_LIKE_POST % (hub_id, new_post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

    def test_get_community_post_likers(self):

        print('Like post...')
        r = requests.post(base_url + COMMUNITY_HUB_LIKE_POST % (hub_id, post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Get likers list
        print('Get post likers...')
        r = requests.get(base_url + COMMUNITY_HUB_LIKERS % (hub_id, post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['results'][0]['user']:
            self.fail('Wrong response.')

    def test_create_community_post_comment(self):

        marker = generate_unique()
        comment = 'Auto API community comment - %s' % marker
        comment_data = '{"text" : "%s"}' % comment

        # Post community comment
        print('Post community comment...')
        url = base_url + COMMUNITY_HUB_POST_COMMENTS % (hub_id, post_id)
        r = requests.post(url, data=comment_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['text'] == comment:
            self.fail('Wrong response.')

    def test_get_community_post_comments(self):

        # Get community post comments
        print('Get community post comments...')
        r = requests.get(base_url + COMMUNITY_HUB_POST_COMMENTS % (hub_id, post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['results'][0]['id'] or not r.json()['results'][0]['text']:
            self.fail('Wrong response.')

    def test_get_community_post_comment(self):

        print('Get community post comments...')
        r = requests.get(base_url + COMMUNITY_HUB_POST_COMMENTS % (hub_id, post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        last_comment_id = r.json()['results'][0]['id']

        # Get community post comment
        print('Get community post comment data...')
        r = requests.get(base_url + COMMUNITY_HUB_POST_COMMENT % (hub_id, post_id, last_comment_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['id'] or not r.json()['text']:
            self.fail('Wrong response.')

    def test_edit_community_post_comment(self):

        marker = generate_unique()
        edited_comment = 'Edited Auto API community comment - %s' % marker
        edited_comment_data = '{"text" : "%s"}' % edited_comment

        # Edit community post comment
        print('Edit community comment...')
        url = base_url + COMMUNITY_HUB_POST_COMMENT % (hub_id, post_id, comment_id)
        r = requests.put(url, data=edited_comment_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['text'] == edited_comment:
            self.fail('Wrong response.')

    def test_delete_community_post_comment(self):

        marker = generate_unique()
        comment = 'Auto API community comment - %s' % marker
        comment_data = '{"text" : "%s"}' % comment

        print('Post community comment...')
        url = base_url + COMMUNITY_HUB_POST_COMMENTS % (hub_id, post_id)
        r = requests.post(url, data=comment_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        new_comment_id = r.json()['id']
        sleep(2)  # DynamoDB delay. Do not remove this sleep(), otherwise test fails sometimes.

        # Delete community post comment
        print('Remove community post comment...')
        r = requests.delete(base_url + COMMUNITY_HUB_POST_COMMENT % (hub_id, post_id, new_comment_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        sleep(2)  # DynamoDB delay. Do not remove this sleep(), otherwise test fails sometimes.

        print('Check if comment still exists...')
        r = requests.get(base_url + COMMUNITY_HUB_POST_COMMENT % (hub_id, post_id, new_comment_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('404', str(r.status_code), msg=logging.debug(r.text))
        # server returns error 404 for removed objects, no need to add additional check

    def test_mark_inappropriate_community_post_comment(self):

        marker = generate_unique()
        comment = 'Auto API community comment - %s' % marker
        comment_data = '{"text" : "%s"}' % comment

        print('Post comment...')
        url = base_url + COMMUNITY_HUB_POST_COMMENTS % (hub_id, post_id)
        r = requests.post(url, data=comment_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        new_comment_id = r.json()['id']

        # Mark comment as inappropriate
        print('Mark comment as inappropriate...')
        url = base_url + COMMUNITY_HUB_INAPPROPRIATE_POST_COMMENT % (hub_id, post_id, new_comment_id)
        r = requests.post(url, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if "Thank you for flagging inappropriate" not in r.json()['message']:
            self.fail('Wrong response.')

    @unittest.skip
    def test_pin_unpin_community_post(self):

        pin_data = '{"expire":"2016-11-23T00:00"}'

        # Pin community post
        print('Pin community post...')
        r = requests.post(base_url + COMMUNITY_HUB_PIN_POST % (hub_id, post_id), data=pin_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if post is pinned
        print('Check if community post is pinned...')
        r = requests.get(base_url + COMMUNITY_HUB_POST % (hub_id, post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['is_pinned']:
            self.fail('Post is not pinned.\n is_pinned: %s' % r.json()['is_pinned'])

        # Unpinning post
        print('Unpin community  post...')
        r = requests.delete(base_url + COMMUNITY_HUB_PIN_POST % (hub_id, post_id), data=pin_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if post is unpinned
        print('Check if community post is unpinned...')
        r = requests.get(base_url + COMMUNITY_HUB_POST % (hub_id, post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['is_pinned']:
            self.fail('Post is not unpinned \n is_pinned : %s' % r.json()['is_pinned'])

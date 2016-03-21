import unittest
import requests
import logging
import json

from time import sleep

from src.api.helpers.unique_gen import *
from src.api.urls.api_urls import *
from src.api.setup.preconditions import Preconditions


class FeedApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        
        global auth, base_url, headers, user_id, user_name,  token

        auth = Preconditions()        
        base_url = auth.env.base_url

        auth.log_in()
        token = auth.token
        headers = {"Authorization": "Token %s" % auth.token, "BKSTG_DISABLE_CACHE": "True"}
        user_id = auth.user_id
        user_name = auth.user_name

        global hub_id, post_id, comment_id

        auth.create_hub(headers)
        hub_id = auth.hub_id

        sleep(1)  # avoid fail on Jenkins

        auth.create_feed_post(headers, hub_id)
        post_id = auth.feed_post_id

        auth.create_feed_post_comment(headers, hub_id, post_id)
        comment_id = auth.feed_post_comment_id
        
        global new_user_id, new_user_name

        auth.create_user()
        new_user_id = auth.new_user_id
        new_user_name = auth.new_user_name

    @classmethod
    def tearDownClass(cls):

        # Delete hub
        print('Delete hub...')
        r = requests.delete(base_url + HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        if '20' not in str(r.status_code):
            raise AssertionError(r.status_code)

    def test_get_feed_posts(self):

        # Get feed posts list
        print('Get feed posts...')
        r = requests.get(base_url + FEED_POSTS_LIST % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['results'][0]['id'] or r.json()['results'][0]['comments']['count'] < 0:
            self.fail('Wrong response.')

    def test_create_feed_post(self):

        marker = generate_unique()
        post_data = {"post_type": "text", "text": "API auto feed post - %s!" % marker, "is_private": False}
        post_json_data = json.dumps(post_data)

        # Create feed post
        print('Create feed post...')
        r = requests.post(base_url + FEED_POSTS_LIST % hub_id, data=post_json_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['text'] == "API auto feed post - %s!" % marker or r.json()['is_private']:
            self.fail('Wrong response.')

    def test_create_post_as_user(self):

        """Add new user to stage team (to be able to post as alias)"""

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

        print('Link user to alias...')
        r = requests.post(base_url + HUB_TEAM_LINK_ALIAS % (hub_id, user_id, new_user_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Check if new user is linked to John Brown alias
        print('Check if user is linked to alias...')
        r = requests.get(base_url + HUB_TEAM_ALIAS % (hub_id, user_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['users'][0]['id'] != new_user_id:
            self.fail('Wrong response.')

        marker = generate_unique()
        post_data = {"post_type": "text", "text": "API auto feed post - %s!" % marker, "is_private": False}
        post_json_data = json.dumps(post_data)

        as_user_headers = {"Authorization": 'Token %s' % token, "AsUser": user_id}

        sleep(1)  # avoid fail on Jenkins

        # Create feed post as user
        print('Create post as user...')
        url = base_url + FEED_POSTS_LIST % hub_id
        r = requests.post(url, data=post_json_data, headers=as_user_headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        post_text = "API auto feed post - %s!" % marker
        post_author = r.json()['author']['username']
        if r.json()['text'] != post_text or post_author != user_name or r.json()['is_private']:
            self.fail('Wrong response.')

        print('Unlink user from alias...')
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

    def test_get_feed_post(self):

        # Get feed post
        print('Get feed post...')
        r = requests.get(base_url + FEED_POST % (hub_id, post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['author'] or not r.json()['id']:
            self.fail('Wrong response.')

    def test_edit_post_comment(self):

        marker = generate_unique()
        edited_comment = 'Edited API auto feed comment - %s' % marker
        payload = '{"text": "%s"}' % edited_comment

        # Edit feed post comment
        print('Edit comment for feed post...')
        r = requests.put(base_url + FEED_POST_COMMENT % (hub_id, post_id, comment_id), data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if 'Edited API auto feed comment - %s' % marker not in r.json()['text']:
            self.fail('Wrong response.')

    @unittest.skip
    def test_switch_feed_post_status(self):

        marker = generate_unique()
        post_data = '{ "post_type":"text","text":"API auto feed post - %s !"}' % marker

        print('Create feed post...')
        r = requests.post(base_url + FEED_POSTS_LIST % hub_id, data=post_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        new_post_id = r.json()['id']
        post_status = 'live'

        # Switch post status to 'live'
        print('Set post status to "%s"' % post_status)
        r = requests.post(base_url + FEED_SWITCH_POST % (hub_id, new_post_id, post_status), headers=headers)
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        print('Status code - %s' % r.status_code, '\n')
        if not r.json()['post_status'] == post_status:
            self.fail('Wrong response.')

        post_status = 'draft'

        # Switch post status to 'draft'
        print('Set post status to "%s"' % post_status)
        r = requests.post(base_url + FEED_SWITCH_POST % (hub_id, new_post_id, post_status), headers=headers)
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        print('Status code - %s' % r.status_code, '\n')
        if not r.json()['post_status'] == post_status:
            self.fail('Wrong response.')

        post_status = 'ready'

        # Switch post status to 'ready'
        print('Set post status to "%s"' % post_status)
        r = requests.post(base_url + FEED_SWITCH_POST % (hub_id, new_post_id, post_status), headers=headers)
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        print('Status code - %s' % r.status_code, '\n')
        if not r.json()['post_status'] == post_status:
            self.fail('Wrong response.')

        post_status = 'scheduled'
        publish_date = '{"publish_datetime" : "2015-12-31T12:29:14+00:00"}'

        # Switch post status to 'scheduled'
        print('Set post status to "%s"' % post_status)
        url = base_url + FEED_SWITCH_POST % (hub_id, new_post_id, post_status)
        r = requests.post(url, data=publish_date, headers=headers)
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        print('Status code - %s' % r.status_code, '\n')
        if not r.json()['post_status'] == post_status:
            self.fail('Wrong response.')

        post_status = 'deleted'

        # Switch post status to 'deleted'
        print('Set post status to "%s"' % post_status)
        r = requests.post(base_url + FEED_SWITCH_POST % (hub_id, new_post_id, post_status), headers=headers)
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        print('Status code - %s' % r.status_code, '\n')
        if not r.json()['post_status'] == post_status:
            self.fail('Wrong response.')

    @unittest.skip
    def test_pin_unpin_feed_post(self):
        
        set_pinned = json.dumps({"pinned": True})

        # Pin feed post
        print('Pin feed post...')
        r = requests.put(base_url + FEED_PIN_POST % (hub_id, post_id), data=set_pinned, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['is_pinned'] == True:
            self.fail('Post is not pinned.')

        set_unpinned = json.dumps({"pinned": False})

        # Unpin feed post
        print('Unpin post...')
        r = requests.put(base_url + FEED_PIN_POST % (hub_id, post_id), data=set_unpinned, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['is_pinned'] == False:
            self.fail(' is_pinned : %s \n Post is not unpinned' % r.json()['is_pinned'])

    def test_get_posts_list_for_admin(self):
        
        # Get list of posts for admin site
        print('Get posts list for admin...')
        r = requests.get(base_url + FEED_POSTS_LIST_FOR_ADMIN % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        if r.json()['results'][0]['hub_id'] != hub_id:
            self.fail('Wrong response.')

    def test_get_post_for_admin(self):
        
        print('Get posts list for admin...')
        r = requests.get(base_url + FEED_POSTS_LIST_FOR_ADMIN % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        new_post_id = r.json()['results'][0]['id']

        # Get feed post for admin
        print('Get feed post for admin...')
        r = requests.get(base_url + FEED_POST_FOR_ADMIN % (hub_id, new_post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['id'] == new_post_id:
            self.fail('Wrong response.')

    def test_get_feed_authors(self):
        
        # Get feed authors
        print('Get feed authors...')
        r = requests.get(base_url + FEED_AUTHORS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['results'][0]['last_name'] or not r.json()['results'][0]['first_name']:
            self.fail('Wrong response.')

    def test_get_feed_post_comments(self):

        # Get feed post comments list
        print('Get feed post comments...')
        r = requests.get(base_url + FEED_POST_COMMENTS_LIST % (hub_id, post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['results'][0]['created'] or not r.json()['results'][0]['author']:
            self.fail('Wrong response.')

    def test_create_feed_post_comment(self):

        comment = 'API auto comment'
        comment_payload = '{"text": "%s"}' % comment

        # Create comment for feed post
        print('Post comment to feed post...')
        url = base_url + FEED_POST_COMMENTS_LIST % (hub_id, post_id)
        r = requests.post(url, data=comment_payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if comment not in r.json()['text']:
            self.fail('Wrong response.')

    def test_get_feed_post_comment(self):

        # Get comment for feed post
        print('Get comment for feed post...')
        r = requests.get(base_url + FEED_POST_COMMENT % (hub_id, post_id, comment_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['id'] != comment_id:
            self.fail('Wrong response.')

    def test_delete_feed_post_comment(self):

        marker = generate_unique()
        comment = 'API auto comment - %s' % marker
        comment_payload = '{"text": "%s"}' % comment

        print('Create feed post comment...')
        url = base_url + FEED_POST_COMMENTS_LIST % (hub_id, post_id)
        r = requests.post(url, data=comment_payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        new_comment_id = r.json()['id']
        sleep(2)  # DynamoDB delay. Do not remove this sleep(), otherwise test fails sometimes.

        # Delete comment for feed post
        print('Remove comment for feed post...')
        r = requests.delete(base_url + FEED_POST_COMMENT % (hub_id, post_id, new_comment_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        sleep(2)  # DynamoDB delay. Do not remove this sleep(), otherwise test fails sometimes.

        print('Check if comment still exists...')
        r = requests.get(base_url + FEED_POST_COMMENT % (hub_id, post_id, new_comment_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('404', str(r.status_code), msg=logging.debug(r.text))
        # server returns error 404 for removed objects, no need to add additional check

    def test_mark_inappropriate_post_comment(self):

        # Mark feed post comment as inappropriate
        print('Mark feed post comment as inappropriate...')
        url = base_url + FEED_REPORT_INAPPROPRIATE_COMMENT % (hub_id, post_id, comment_id)
        r = requests.post(url, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if "Thank you for flagging inappropriate content" not in r.json()['message']:
            self.fail('Wrong response.')

    def test_get_feed_likers(self):

        print('Like feed post...')
        r = requests.post(base_url + FEED_POST_LIKES % (hub_id, post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Get feed post likers
        print('Get feed post likers...')
        r = requests.get(base_url + FEED_POST_LIKES % (hub_id, post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['results'][0]['user']['username']:
            self.fail('Wrong response.')

    def test_like_unlike_feed_post(self):

        # Like feed post
        print('Like feed post...')
        r = requests.post(base_url + FEED_POST_LIKES % (hub_id, post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        # Unlike feed post
        print('Unlike feed post...')
        r = requests.delete(base_url + FEED_POST_LIKES % (hub_id, post_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

    @unittest.skip
    def test_edit_feed_post(self):

        marker = generate_unique()
        raw = {"post_type": "text", "text": "Edited API auto feed post - %s" % marker, "is_premium": "false"}
        payload = json.dumps(raw)

        # Edit feed post
        print('Edit feed post...')
        r = requests.put(base_url + FEED_POST % (hub_id, post_id), data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['text'] == 'Edited API auto feed post - %s' % marker:
            self.fail('Wrong response.')

    def test_get_push_messages_list(self):

        # Get push messages
        print('Get push messages...')
        r = requests.get(base_url + FEED_PUSHES % (hub_id, user_id), headers=headers)
        audio = r.json()['audio']
        image = r.json()['image']
        text = r.json()['text']
        video = r.json()['video']
        if 'audio' not in audio or 'pic' not in image or 'post' not in text or 'vid' not in video:
            self.fail('Wrong response')

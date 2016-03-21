import unittest
import json
import requests
import logging

from src.api.helpers.unique_gen import *
from src.api.helpers.upload_to_sandbox import Upload
from src.api.urls.api_urls import *
from src.api.setup.preconditions import Preconditions
from src.api.setup.test_data import TestData


@unittest.skip
class MediaApiTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        global auth, base_url, headers, hub_id, user_id

        auth = Preconditions()
        base_url = auth.env.base_url

        auth.log_in()
        headers = {"Authorization": "Token %s" % auth.token, "BKSTG_DISABLE_CACHE": "True"}
        user_id = auth.user_id

        auth.create_hub(headers)
        hub_id = auth.hub_id

        global cover, image_id, audio_id, video_id, image_key, thumbnail_id

        cover = TestData.album_cover

        auth.upload_image(TestData.image_path)
        image_key = auth.image_key
        image_id = auth.image_id

        auth.upload_video(TestData.video_path)
        video_id = auth.video_id

        auth.upload_audio(TestData.audio_path)
        audio_id = auth.audio_id

        auth.upload_thumbnail(TestData.thumbnail_path)
        thumbnail_id = auth.thumbnail_id

    @classmethod
    def tearDownClass(cls):

        # Delete hub
        print('Delete hub...')
        r = requests.delete(base_url + HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        if '20' not in str(r.status_code):
            raise AssertionError(r.status_code)

    def test_add_external_video(self):

        video_url = TestData.ext_video_1_url
        payload = json.dumps(video_url)

        # Add video from external resource
        print('Add video from external resource...')
        r = requests.post(base_url + MEDIA_EXT_RESOURCE, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['item']['content_type'] != "web_video" or r.json()['item']['title'] != TestData.ext_video_1_name:
            self.fail('Wrong response.')

    def test_add_external_audio(self):

        audio_url = TestData.ext_audio_1_url
        payload = json.dumps(audio_url)

        # Add audio from external resource
        print('Add audio from external resource...')
        r = requests.post(base_url + MEDIA_EXT_RESOURCE, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['item']['content_type'] != "web_audio" or r.json()['item']['title'] != TestData.ext_audio_1_name:
            self.fail('Wrong response.')

    def test_hub_add_ext_video(self):

        video_url = TestData.ext_video_2_url
        payload = json.dumps(video_url)

        # Add external video for hub
        print('Add external video for hub...')
        r = requests.post(base_url + MEDIA_HUB_EXT_RESOURCE % hub_id, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['item']['content_type'] != "web_video" or r.json()['item']['title'] != TestData.ext_video_2_name:
            self.fail('Wrong response.')

    def test_hub_add_ext_audio(self):

        audio_url = TestData.ext_audio_2_url
        payload = json.dumps(audio_url)

        # Add external audio for hub
        print('Add external audio for hub...')
        r = requests.post(base_url + MEDIA_HUB_EXT_RESOURCE % hub_id, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['item']['content_type'] != "web_audio" or r.json()['item']['title'] != TestData.ext_audio_2_name:
            self.fail('Wrong response.')

    def test_after_upload_image(self):

        key = Upload.upload_to_sandbox(path=TestData.image_path)
        image_data = {"key": "%s" % key,
                      "title": "background",
                      "mime_type": "image/jpeg",
                      "width": 1500,
                      "height": 1000
                      }
        payload = json.dumps(image_data)

        # After upload
        print('After upload image...')
        r = requests.post(base_url + MEDIA_AFTER_UPLOAD, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['item']['content_type'] != 'image' or r.json()['item']['title'] != 'background':
            self.fail('Wrong response.')

    def test_after_upload_video(self):

        key = Upload.upload_to_sandbox(path=TestData.video_path)
        video_data = {"sources": [{"key": "%s" % key,
                                   "type": "s3"}],
                      "title": "Video",
                      "type": "video",
                      "mime_type": "video/mp4"
                      }
        payload = json.dumps([video_data])

        # After upload
        print('After upload video...')
        r = requests.post(base_url + MEDIA_ITEMS_LIST, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()[0]['type'] != 'video' or r.json()[0]['title'] != 'Video':
            self.fail('Wrong response.')

    def test_attach_thumbnail(self):

        # Attach thumbnail to video
        print('Attach thumbnail...')
        url = base_url + MEDIA_ITEM_THUMBNAIL % video_id
        thumbnail = {"image_id": "%s" % thumbnail_id}
        payload = json.dumps(thumbnail)
        r = requests.put(url, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['thumbnail']['content_type'] != 'image':
            self.fail('Wrong response.')

    def test_attach_preview(self):

        # Attach preview to video
        print('Attach preview...')
        url = base_url + MEDIA_ITEM_PREVIEW % video_id
        preview = {"preview_id": "%s" % video_id}
        payload = json.dumps(preview)
        r = requests.put(url, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['preview']['content_type'] != 'native_video':
            self.fail('Wrong response.')

    def test_get_items_list(self):

        # Get items list
        print('Get items list...')
        r = requests.get(base_url + MEDIA_ITEMS_LIST, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['results'][0]['id']:
            self.fail('Wrong response.')

    def test_get_sandbox_settings(self):

        # Get sandbox settings
        print('Get sandbox settings...')
        r = requests.get(base_url + MEDIA_SANDBOX, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['aws-access-key'] or r.json()['bucket'] != "bkstg-sandbox":
            self.fail('Wrong response.')

    """ Create media albums tests """

    def test_create_image_album(self):

        marker = generate_unique()
        image_album_title = 'New Image Album %s' % marker
        payload = json.dumps({"title": image_album_title, "cover": cover, "is_public": True})

        # Create image album
        print('Create image album...')
        r = requests.post(base_url + MEDIA_IMAGE_ALBUMS % hub_id, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['title'] != image_album_title or r.json()['type'] != 'image':
            self.fail('Wrong response.')
        self.image_album_id = r.json()['id']

    def test_create_audio_album(self):

        marker = generate_unique()
        audio_album_title = 'New Audio Album %s' % marker
        payload = json.dumps({"title": audio_album_title, "cover": cover, "is_public": True})

        # Create audio album
        print('Create audio album...')
        r = requests.post(base_url + MEDIA_AUDIO_ALBUMS % hub_id, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['title'] != audio_album_title or r.json()['type'] != 'audio':
            self.fail('Wrong response.')
        self.audio_album_id = r.json()['id']

    def test_create_video_album(self):

        marker = generate_unique()
        video_album_title = 'New Video Album %s' % marker
        payload = json.dumps({"title": video_album_title, "cover": cover, "is_public": True})

        # Create video album
        print('Create video album...')
        r = requests.post(base_url + MEDIA_VIDEO_ALBUMS % hub_id, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()['title'] != video_album_title or r.json()['type'] != 'video':
            self.fail('Wrong response.')
        self.video_album_id = r.json()['id']

    """ Edit media albums tests """

    def test_edit_image_album(self):

        self.test_create_image_album()

        print('Get image albums for hub...')
        r = requests.get(base_url + MEDIA_IMAGE_ALBUMS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        image_album_id = r.json()[0]['id']

        marker = generate_unique()
        image_album_title = 'Edited Image Album %s' % marker
        raw = {"title": "%s" % image_album_title,
               "id": "%s" % image_album_id,
               "is_public": True
               }
        payload = json.dumps(raw)

        # Edit image album
        print('Edit hub image album...')
        url = base_url + MEDIA_IMAGE_ALBUMS % hub_id
        r = requests.put(url, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()[0]['title'] != image_album_title or r.json()[0]['type'] != 'image':
            self.fail('Wrong response.')

    def test_edit_audio_album(self):

        self.test_create_audio_album()

        print('Get audio albums for hub...')
        r = requests.get(auth.env.base_url + MEDIA_AUDIO_ALBUMS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        audio_album_id = r.json()[0]['id']

        marker = generate_unique()
        audio_album_title = 'Edited Audio Album %s' % marker
        raw = {"title": "%s" % audio_album_title,
               "id": "%s" % audio_album_id,
               "is_public": True
               }
        payload = json.dumps(raw)

        # Edit audio album
        print('Edit hub audio album...')
        url = base_url + MEDIA_AUDIO_ALBUMS % hub_id
        r = requests.put(url, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()[0]['title'] != audio_album_title or r.json()[0]['type'] != 'audio':
            self.fail('Wrong response.')

    def test_edit_video_album(self):

        self.test_create_video_album()

        print('Get video albums for hub...')
        r = requests.get(auth.env.base_url + MEDIA_VIDEO_ALBUMS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        video_album_id = r.json()[0]['id']

        marker = generate_unique()
        video_album_title = 'Edited Video Album %s' % marker
        raw = {"title": "%s" % video_album_title,
               "id": "%s" % video_album_id,
               "is_public": True
               }
        payload = json.dumps(raw)

        # Edit video album
        print('Edit hub video album...')
        url = base_url + MEDIA_VIDEO_ALBUMS % hub_id
        r = requests.put(url, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()[0]['title'] != video_album_title or r.json()[0]['type'] != 'video':
            self.fail('Wrong response.')

    """ Delete media albums tests """

    def test_delete_image_album(self):

        self.test_create_image_album()

        print('Get image albums for hub...')
        r = requests.get(base_url + MEDIA_IMAGE_ALBUMS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        image_album_id = r.json()[0]['id']

        # Remove image album
        print('Remove hub image album...')
        r = requests.delete(base_url + MEDIA_HUB_IMAGE_ALBUM % (hub_id, image_album_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        print('Get image albums for hub...')
        r = requests.get(base_url + MEDIA_IMAGE_ALBUMS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.text != "[]" and r.json()[0]['id'] == image_album_id:
            self.fail('Wrong response.')

    def test_delete_audio_album(self):

        self.test_create_audio_album()

        print('Get audio albums for hub...')
        r = requests.get(base_url + MEDIA_AUDIO_ALBUMS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        audio_album_id = r.json()[0]['id']

        # Remove audio album
        print('Remove hub audio album...')
        r = requests.delete(base_url + MEDIA_HUB_AUDIO_ALBUM % (hub_id, audio_album_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        print('Get audio albums for hub...')
        r = requests.get(base_url + MEDIA_AUDIO_ALBUMS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.text != "[]" and r.json()[0]['id'] == audio_album_id:
            self.fail('Wrong response.')

    def test_delete_video_album(self):

        self.test_create_video_album()

        print('Get video albums for hub...')
        r = requests.get(base_url + MEDIA_VIDEO_ALBUMS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        video_album_id = r.json()[0]['id']

        # Remove video album
        print('Remove hub video album...')
        r = requests.delete(base_url + MEDIA_HUB_VIDEO_ALBUM % (hub_id, video_album_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

        print('Get video albums for hub...')
        r = requests.get(base_url + MEDIA_VIDEO_ALBUMS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.text != "[]" and r.json()[0]['id'] == video_album_id:
            self.fail('Wrong response.')

    """ Attach media file to albums """

    def test_attach_image_to_album(self):

        self.test_create_image_album()

        images = {"items": ["%s" % image_id]}
        payload = json.dumps(images)

        # Attach image to album
        print('Attach image to album...')
        url = base_url + MEDIA_ALBUM_ATTACH_IMAGE_ITEMS % (hub_id, self.image_album_id)
        r = requests.post(url, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('201', str(r.status_code), msg=logging.debug(r.text))

    def test_attach_audio_to_album(self):

        self.test_create_audio_album()

        audios = {"items": ["%s" % audio_id]}
        payload = json.dumps(audios)

        # Attach audio to album
        print('Attach audio to album...')
        url = base_url + MEDIA_ALBUM_ATTACH_AUDIO_ITEMS % (hub_id, self.audio_album_id)
        r = requests.post(url, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('201', str(r.status_code), msg=logging.debug(r.text))

    def test_attach_video_to_album(self):

        self.test_create_video_album()

        videos = {"items": ["%s" % video_id]}
        payload = json.dumps(videos)

        # Attach video to album
        print('Attach image to album...')
        url = base_url + MEDIA_ALBUM_ATTACH_VIDEO_ITEMS % (hub_id, self.video_album_id)
        r = requests.post(url, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('201', str(r.status_code), msg=logging.debug(r.text))

    """ Get media albums tests """

    def test_get_image_albums(self):

        self.test_create_image_album()

        # Get image albums for hub
        print('Get image albums for hub...')
        r = requests.get(base_url + MEDIA_IMAGE_ALBUMS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if 'Image' not in r.json()[0]['title']:
            self.fail('Wrong response.')

    def test_get_audio_albums(self):

        self.test_create_audio_album()

        # Get audio albums for hub
        print('Get audio albums for hub...')
        r = requests.get(base_url + MEDIA_AUDIO_ALBUMS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if 'Audio' not in r.json()[0]['title']:
            self.fail('Wrong response.')

    def test_get_video_albums(self):

        self.test_create_video_album()

        # Get video albums for hub
        print('Get video albums for hub...')
        r = requests.get(base_url + MEDIA_VIDEO_ALBUMS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if 'Video' not in r.json()[0]['title']:
            self.fail('Wrong response.')

    def test_get_image_album(self):

        self.test_create_image_album()

        # Get image albums for hub
        print('Get image album...')
        r = requests.get(base_url + MEDIA_IMAGE_ALBUM % (hub_id, self.image_album_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()[0]['id'] != self.image_album_id:
            self.fail('Wrong response.')

    def test_get_audio_album(self):

        self.test_create_audio_album()

        # Get image albums for hub
        print('Get image album...')
        r = requests.get(base_url + MEDIA_AUDIO_ALBUM % (hub_id, self.audio_album_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()[0]['id'] != self.audio_album_id:
            self.fail('Wrong response.')

    def test_get_video_album(self):

        self.test_create_video_album()

        # Get image albums for hub
        print('Get image album...')
        r = requests.get(base_url + MEDIA_VIDEO_ALBUM % (hub_id, self.video_album_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()[0]['id'] != self.video_album_id:
            self.fail('Wrong response.')

    """ Attach media files to hub tests """

    def test_attach_image_to_hub(self):

        images = {"items": ["%s" % image_id]}
        payload = json.dumps(images)

        # Attach image to hub
        print('Attach image to hub...')
        r = requests.post(base_url + MEDIA_HUB_ATTACH_IMAGE_ITEMS % hub_id, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('201', str(r.status_code), msg=logging.debug(r.text))

    def test_attach_audio_to_hub(self):

        audios = {"items": ["%s" % audio_id]}
        payload = json.dumps(audios)

        # Attach audio to hub
        print('Attach audio to hub...')
        r = requests.post(base_url + MEDIA_HUB_ATTACH_AUDIO_ITEMS % hub_id, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('201', str(r.status_code), msg=logging.debug(r.text))

    def test_attach_video_to_hub(self):

        videos = {"items": ["%s" % video_id]}
        payload = json.dumps(videos)

        # Attach video to hub
        print('Attach video to hub...')
        r = requests.post(base_url + MEDIA_HUB_ATTACH_VIDEO_ITEMS % hub_id, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))

    """ Get hub media tests """

    def test_get_hub_image_items(self):

        self.test_attach_image_to_hub()

        # Make image public
        print('Make image public...')
        edit_data = json.dumps({"id": image_id, "is_public": True})
        r = requests.put(base_url + MEDIA_HUB_IMAGE_ITEMS % hub_id, data=edit_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()[0]['is_public']:
            self.fail('Image is not public')

        # Get media images for hub
        print('Get images for hub ...')
        r = requests.get(base_url + MEDIA_HUB_IMAGE_ITEMS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()[0]['id'] != image_id or r.json()[0]['content_type'] != 'image':
            self.fail('Wrong response.')

    def test_get_hub_audio_items(self):

        self.test_attach_audio_to_hub()

        # Make audio public
        print('Make audio public...')
        edit_data = json.dumps({"id": audio_id, "is_public": True})
        r = requests.put(base_url + MEDIA_HUB_AUDIO_ITEMS % hub_id, data=edit_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()[0]['is_public']:
            self.fail('Audio is not public.')

        # Get media audios for hub
        print('Get audio records for hub...')
        r = requests.get(base_url + MEDIA_HUB_AUDIO_ITEMS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()[0]['id'] != audio_id or r.json()[0]['content_type'] != 'native_audio':
            self.fail('Wrong response.')

    def test_get_hub_video_items(self):

        self.test_attach_video_to_hub()

        # Make videos public
        print('Make video public...')
        edit_data = json.dumps({"id": video_id, "is_public": True})
        r = requests.put(base_url + MEDIA_HUB_VIDEO_ITEMS % hub_id, data=edit_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()[0]['is_public']:
            self.fail('Video is not public')

        # Get videos for hub
        print('Get videos for hub...')
        r = requests.get(base_url + MEDIA_HUB_VIDEO_ITEMS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()[0]['id'] != video_id or r.json()[0]['content_type'] != 'native_video':
            self.fail('Wrong response.')

    def test_get_image_album_items(self):

        self.test_attach_image_to_album()

        print('Make image public...')
        url = base_url + MEDIA_ALBUM_IMAGE_ITEMS % (hub_id, self.image_album_id)
        payload = json.dumps({"id": image_id, "is_public": True})
        r = requests.put(url, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()[0]['is_public']:
            self.fail('Wrong response.')

        # Get image album items
        print('Get image album items...')
        r = requests.get(base_url + MEDIA_ALBUM_IMAGE_ITEMS % (hub_id, self.image_album_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()[0]['id'] != image_id:
            self.fail('Wrong response.')

    """ Get album media tests """

    def test_get_audio_album_items(self):

        self.test_attach_audio_to_album()

        print('Make audio public...')
        url = base_url + MEDIA_ALBUM_AUDIO_ITEMS % (hub_id, self.audio_album_id)
        payload = json.dumps({"id": audio_id, "is_public": True})
        r = requests.put(url, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()[0]['is_public']:
            self.fail('Wrong response.')

        # Get audio album items
        print('Get audio album items...')
        r = requests.get(base_url + MEDIA_ALBUM_AUDIO_ITEMS % (hub_id, self.audio_album_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()[0]['id'] != audio_id:
            self.fail('Wrong response.')

    def test_get_video_album_items(self):

        self.test_attach_video_to_album()

        print('Make video public...')
        url = base_url + MEDIA_ALBUM_VIDEO_ITEMS % (hub_id, self.video_album_id)
        payload = json.dumps({"id": video_id, "is_public": True})
        r = requests.put(url, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()[0]['is_public']:
            self.fail('Wrong response.')

        # Get video album items
        print('Get video album items...')
        r = requests.get(base_url + MEDIA_ALBUM_VIDEO_ITEMS % (hub_id, self.video_album_id), headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()[0]['id'] != video_id:
            self.fail('Wrong response.')

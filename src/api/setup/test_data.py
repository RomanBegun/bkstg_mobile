import os

import sys


class TestData(object):

    # Accounts

    device_id = 'c9eaeab4-e3ca-9abc-6004-7b3400000000'
    device_token = 'edcpl9_tXPE:APA91bHFV-CGwoF0QdRbJu2UU-aM4uOqFt96vsY2mqF-1mMnKwlssdb2UqGgFXuhy1cZCxMRCRAEbTGYo8Hk' \
                   '2nU9XXiOk3UJwUYpN7oXfT-MtvlqUlprvu5m9XHcGSc5ALlQ_li-lTmr'

    facebook_app_id = '487428034762168'
    facebook_app_secret = '55d985d0d10f5d79e71ea85dcfb8ace2'
    access_token = '1785539405006138|VBuxUBQfpigKhX2DnLJKI0d8V2c'

    # Auth

    email = "roma@bkstg.com"
    password = "12345678"
    admin_id = '498a017d-3f5b-43a8-a8c7-86a2136f28b7'

    celebrity_email = 'Celebrity1@bkstg.com'
    celebrity_password = '12345678'

    # Media

    image_path = os.path.join(sys.path[0], '../../test_files/image/background.jpg')
    video_path = os.path.join(sys.path[0], '../../test_files/video/10.mp4')
    thumbnail_path = os.path.join(sys.path[0], '../../test_files/video/10.jpg')
    audio_path = os.path.join(sys.path[0], '../../test_files/audio/1.mp3')

    album_cover = '{"content_type": "thumbnail_image", ' \
            '"data": null, "external_id": ' \
            '"ieSQwupV8-4", "id": "6c1e6ea3-2b87-468e-9114-19823c66ecb4", ' \
            '"mime_type": "video/mpeg", ' \
            '"preview": null, ' \
            '"thumbnail": null, ' \
            '"title": "Automated API Test", ' \
            '"url": null' \
            '}'

    ext_video_1_url = {'url': 'https://www.youtube.com/watch?v=VDvr08sCPOc'}
    ext_video_1_name = "Fort Minor - Remember The Name (Official Video)"

    ext_video_2_url = {'url': 'https://www.youtube.com/watch?v=1wYNFfgrXTI'}
    ext_video_2_name = "Eminem - When I'm Gone"

    ext_audio_1_url = {'url': 'https://soundcloud.com/dgotw/marcela-mangabeira-poker-face'}
    ext_audio_1_name = "Marcela Mangabeira - Poker Face by Drowned Girl On The Web"

    ext_audio_2_url = {'url': 'https://soundcloud.com/theglitchmob/the-glitch-mob-our-demons-feat'}
    ext_audio_2_name = "The Glitch Mob - Our Demons (feat. Aja Volkman) by The Glitch Mob"

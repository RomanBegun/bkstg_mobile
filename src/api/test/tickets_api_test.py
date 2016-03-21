import json
import unittest
import requests
import logging

from src.api.setup.test_data import TestData
from src.api.helpers.unique_gen import *
from src.api.urls.api_urls import *
from src.api.setup.preconditions import Preconditions


class TicketsApiTest(unittest.TestCase):

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
        
        global image_id, image_item
        
        auth.upload_image(TestData.image_path)
        image_id = auth.image_id
        image_item = auth.image_item

    @classmethod
    def tearDownClass(cls):

        # Delete hub
        print('Delete hub...')
        r = requests.delete(base_url + HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        if '20' not in str(r.status_code):
            raise AssertionError(r.status_code)

    def test_get_tour(self):

        # Get tour and related concerts
        print('Get tour and related concerts...')
        r = requests.get(base_url + TICKETS_HUB_TOUR % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['id'] or r.json()['on_tour']:
            self.fail('Wrong response.')

    def test_update_tour(self):

        # Get tour and related concerts
        print('Get tour and related concerts...')
        r = requests.get(base_url + TICKETS_HUB_TOUR % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['id'] or r.json()['on_tour']:
            self.fail('Wrong response.')

        self.tour_id = r.json()['id']

        marker = generate_unique()
        tour_title = 'Auto API Tour %s' % marker
        tour_data = {"title": tour_title,
                     "on_tour": True,
                     "description": "Test Tour Description",
                     "cover_id": image_id}
        payload = json.dumps(tour_data)

        # Update tour data
        print('Update tour data...')
        r = requests.put(base_url + TICKETS_HUB_TOUR % self.tour_id, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        exp_tour_response = {"title": tour_title,
                             "on_tour": True,
                             "description": "Test Tour Description",
                             "cover": image_item}
        if not exp_tour_response.items() <= r.json().items():
            self.fail('Wrong response.')

    def test_create_concert(self):

        # Get tour and related concerts
        print('Get tour and related concerts...')
        r = requests.get(base_url + TICKETS_HUB_TOUR % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not r.json()['id'] or r.json()['on_tour']:
            self.fail('Wrong response.')

        self.tour_id = r.json()['id']

        concert_data = {"city": "Los Angeles",
                        "country": "USA",
                        "date": "2017-12-23",
                        "state": "California",
                        "venue": "Bkstg Office",
                        "tickets_url": "http://ticketmaster.com",
                        "is_tickets_sold_out": False,
                        "is_public": True
                        }
        payload = json.dumps(concert_data)

        # Create new concert
        print('Create new concert...')
        r = requests.post(base_url + TICKETS_TOUR_CONCERTS % self.tour_id, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not concert_data.items() <= r.json().items():
            self.fail('Wrong response.')
        self.concert_id = r.json()['id']

    def test_edit_concert(self):

        self.test_create_concert()

        edited_concert_data = {"id": "%s" % self.concert_id,
                               "city": "New York",
                               "country": "USA",
                               "date": "2017-12-25",
                               "state": "New York",
                               "venue": "Bkstg Office",
                               "tickets_url": "http://ticketmaster.com",
                               "is_tickets_sold_out": True,
                               "is_public": True
                               }
        payload = json.dumps(edited_concert_data)

        # Edit concert
        print('Edit concert...')
        r = requests.put(base_url + TICKETS_TOUR_CONCERTS % self.tour_id, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if not edited_concert_data.items() <= r.json()[0].items():
            self.fail('Wrong response.')

    def test_tickets_delete_concert(self):

        self.test_create_concert()

        payload = json.dumps(self.concert_id)

        # Delete concert
        print('Delete concert...')
        r = requests.delete(base_url + TICKETS_TOUR_CONCERTS % self.tour_id, data=payload, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()[0] != self.concert_id:
            self.fail('Wrong response.')

        print('Check if concert is deleted...')
        r = requests.get(base_url + TICKETS_HUB_TOUR % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        concert_len = len(r.json()['concerts'])

        # check if concert is removed
        if concert_len >= 1:
            for i in (0, concert_len - 1):  # case when recently created concert was NOT the only concert in tour
                if r.json()['concerts'][i]['id'] == self.concert_id:
                    self.fail('Concert is not deleted')
        elif r.json()['concerts']:  # case when recently created concert was the only concert in tour
                self.fail('Concert is not deleted')

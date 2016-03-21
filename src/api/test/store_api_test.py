import json
import unittest
import requests
import logging

from src.api.setup.test_data import TestData
from src.api.helpers.unique_gen import *
from src.api.urls.api_urls import *
from src.api.setup.preconditions import Preconditions


class StoreApiTest(unittest.TestCase):

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

        global image_item

        auth.upload_image(TestData.image_path)
        image_item = auth.image_item

    @classmethod
    def tearDownClass(cls):
        
        # Delete hub
        print('Delete hub...')
        r = requests.delete(base_url + HUB % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        if '20' not in str(r.status_code):
            raise AssertionError(r.status_code)

    def test_add_store_product(self):

        image_id = image_item['id']
        marker = generate_unique()
        product_data = {"name": "Test Product %s" % marker,
                        "description": "Test Product Description %s" % marker,
                        "price": 99.99,
                        "currency": "USD",
                        "url": "http://bkstg.com",
                        "tags": ["test_tag1", "test_tag2"],
                        "is_public": True,
                        "image_id": image_id
                        }
        product_data_json = json.dumps(product_data)

        # Add store product
        print('Add store product...')
        r = requests.post(base_url + STORE_PRODUCTS % hub_id, data=product_data_json, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        exp_product_response = {"name": "Test Product %s" % marker,
                                "description": "Test Product Description %s" % marker,
                                "price": 99.99,
                                "currency": "USD",
                                "url": "http://bkstg.com",
                                "tags": ["test_tag1", "test_tag2"],
                                "is_public": True,
                                "image": image_item
                                }
        if not exp_product_response.items() <= r.json().items():
            self.fail('Wrong response.')
            
        self.product_id = r.json()['id']

        # Check if store product is added
        print('Check if store product is added...')
        r = requests.get(base_url + STORE_PRODUCTS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        products_len = len(r.json())
        self.product_items = ''
        for i in range(products_len):
            if exp_product_response.items() <= r.json()[i].items():
                self.product_items = r.json()[i].items()
        if not exp_product_response.items() <= self.product_items:
                self.fail('Wrong response.')

    def test_edit_store_product(self):
        
        self.test_add_store_product()

        image_id = image_item['id']
        marker = generate_unique()
        edited_product_data = {"id": self.product_id,
                               "name": "Edited Test Product %s" % marker,
                               "description": "Edited Test Product Description %s" % marker,
                               "price": 199.99,
                               "currency": "GBP",
                               "url": "http://manage.bkstg.com",
                               "tags": ["edited_test_tag1", "edited_test_tag2"],
                               "is_public": True,
                               "image_id": image_id
                               }
        product_data_json = json.dumps(edited_product_data)

        # Edit store product
        print('Edit store product...')
        r = requests.put(base_url + STORE_PRODUCTS % hub_id, data=product_data_json, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        exp_edited_response = {"id": self.product_id,
                                "name": "Edited Test Product %s" % marker,
                                "description": "Edited Test Product Description %s" % marker,
                                "price": 199.99,
                                "currency": "GBP",
                                "url": "http://manage.bkstg.com",
                                "tags": ["edited_test_tag1", "edited_test_tag2"],
                                "is_public": True,
                                "image": image_item
                                }
        if not exp_edited_response.items() <= r.json()[0].items():
            self.fail('Wrong response.')

        # Check if store product is edited
        print('Check if edited store product is saved...')
        r = requests.get(base_url + STORE_PRODUCTS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        results_len = len(r.json())
        for i in range(results_len):
            if r.json()[i]['id'] == self.product_id:
                if not exp_edited_response.items() <= r.json()[i].items():
                    self.fail('Wrong response.')

    def test_delete_store_product(self):

        self.test_add_store_product()

        delete_product_data = json.dumps(self.product_id)

        # Delete store product
        print('Delete store product...')
        r = requests.delete(base_url + STORE_PRODUCTS % hub_id, data=delete_product_data, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        if r.json()[0] != self.product_id:
            self.fail('Product is not deleted.')

        # Check if store product is deleted
        print('Check if store product is deleted...')
        r = requests.get(base_url + STORE_PRODUCTS % hub_id, headers=headers)
        print('Status code - %s' % r.status_code, '\n')
        self.assertIn('20', str(r.status_code), msg=logging.debug(r.text))
        products_len = len(r.json())
        if products_len >= 1:
            for i in (0, products_len - 1):
                if r.json()[i]['id'] == self.product_id:
                    self.fail('Product is not deleted.')
        elif r.json():
                self.fail('Product is not deleted.')

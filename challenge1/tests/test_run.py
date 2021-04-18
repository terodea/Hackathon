import unittest
import requests
import json
import pdb
from configs.data_model import TestValidateDataModel
class TestConfig:
    API_URL = "http://127.0.0.1:5000/course"
    COURSE_OBJ = {
        "description": "This is a brand new course",
        "discount_price": 5,
        "title": "Brand new course",
        "price": 25,
        "image_path": "images/some/path/foo.jpg",
        "on_discount": False
    }
    BAD_COURSE_OBJ = {
        "description": "This is a brand new course",
        "discount_price": 5,
        "title": "Brand new course",
        "price": "this_should_be_integer",
        "image_path": "images/some/path/foo.jpg",
        "on_discount": False
    }
    UPDATE_COURSE = {
        "image_path": "images/some/path/foo.jpg",
        "discount_price": 5,
        "id": 17,
        "price": 25,
        "title": "Blah blah blah",
        "on_discount": False,
        "description": "New description"
    }
    BAD_PRICE_UPDATE_COURSE = {
        "image_path": "images/some/path/foo.jpg",
        "discount_price": 5,
        "id": 17,
        "price": "this_should_be_integer",
        "title": "Blah blah blah",
        "on_discount": False,
        "description": "New description"
    }
    BAD_IMAGE_PATH_ADD_COURSE = {
        "image_path": "images/some/path/foo.jpg/images/some/path/foo.jpg/images/some/path/foo.jpg/images/some/path/foo.jpg/images/some/path/foo.jpg/images/some/path/foo.jpg/images/some/path/foo.jpg/images/some/path/foo.jpg/images/some/path/foo.jpg/images/some/path/foo.jpg/images/some/path/foo.jpg",
        "discount_price": 5,
        "price": "this_should_be_integer",
        "title": "Blah blah blah",
        "on_discount": False,
        "description": "New description"
    }

is_data_modle_valid = TestValidateDataModel()

class RunTest(unittest.TestCase):
    def test_get_course_by_id(self):
        id = 101
        r = requests.get(TestConfig.API_URL + f"/{id}")
        response = json.loads(r._content)['data']
        is_valid = is_data_modle_valid.validate(response)
        self.assertEqual(is_valid, {})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers["Content-Type"], 'application/json')

    def test_get_course_invalid_id(self):
        id = -20
        r = requests.get(TestConfig.API_URL + f"/{id}")
        self.assertEqual(r.status_code, 404)

    def test_delete_course(self):
        id = 62
        r = requests.delete(TestConfig.API_URL + f"/{id}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers["Content-Type"], 'application/json')

    def test_add_course(self):
        r = requests.post(TestConfig.API_URL, data=json.dumps(TestConfig.COURSE_OBJ))
        self.assertEqual(r.status_code, 201)

    def test_invalid_price(self):
        r = requests.post(TestConfig.API_URL, data=json.dumps(TestConfig.BAD_COURSE_OBJ))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()["message"], "Not a valid integer. ")

    def test_invalid_image_path(self):
        r = requests.post(TestConfig.API_URL,
                          data=json.dumps(TestConfig.BAD_IMAGE_PATH_ADD_COURSE))
        
        self.assertEqual(r.status_code, 400)

    def test_update_course(self):
        id = TestConfig.UPDATE_COURSE["id"]
        r = requests.put(TestConfig.API_URL +
                         f"/{id}", data=json.dumps(TestConfig.UPDATE_COURSE))
        self.assertEqual(r.status_code, 200)

    def test_update_bad_course(self):
        id = TestConfig.BAD_PRICE_UPDATE_COURSE["id"]
        r = requests.put(TestConfig.API_URL +
                         f"/{id}", data=json.dumps(TestConfig.BAD_PRICE_UPDATE_COURSE))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.json()["message"], "Not a valid integer. ")

    def test_no_of_page_of_courses(self):
        r = requests.get(TestConfig.API_URL, params={
                         "page-number": "20", "page-size": "10"})
        response = json.loads(r._content)['data']
        self.assertEqual(len(response), 10)
        self.assertAlmostEqual([i['id'] for i in response], [192, 193, 194, 195, 196, 197, 198, 199, 200, 201])
        self.assertEqual(r.status_code, 200)

    def test_default_page_of_courses(self):

        r = requests.get(TestConfig.API_URL)
        response = json.loads(r._content)['data']
        self.assertEqual(len(response), 10)
        self.assertAlmostEqual([i['id'] for i in response], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(r.status_code, 200)
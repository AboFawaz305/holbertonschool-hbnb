import unittest, requests
from config import DevelopmentConfig


class TestUserEndpoint(unittest.TestCase):
    def test_get_root_accasable(self):
        requests.get(DevelopmentConfig.API_URL)
        requests.get(DevelopmentConfig.API_URL + "/")

    def test_get_root_201(self):
        res = requests.get(DevelopmentConfig.API_URL + "/")

    def test_post_root_201(self):
        res = requests.post(
            DevelopmentConfig.API_URL + "/api/v1/users/",
            json={"first_name": "11", "last_name": "22", "email": "ddda@gmail.com"},
        )
        self.assertEqual(res.status_code, 201)

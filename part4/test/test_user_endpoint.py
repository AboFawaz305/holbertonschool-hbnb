import unittest
import requests
from config import DevelopmentConfig

class TestUserEndpoint(unittest.TestCase):
    def test_get_root_accessible(self):
        """Check if the root URL responds with status 200"""
        res = requests.get(DevelopmentConfig.API_URL + "/")
        self.assertEqual(res.status_code, 200)

    def test_get_root_201(self):
        """(If expected) Check if root returns 201 — adjust if needed"""
        res = requests.get(DevelopmentConfig.API_URL + "/")
        self.assertEqual(res.status_code, 201)
    def test_post_root_201(self):
        """POST /api/v1/users/ should return 201 on success"""
        res = requests.post(
            DevelopmentConfig.API_URL + "/api/v1/users/",
            json={
                "first_name": "11",
                "last_name": "22",
                "email": "ddda@gmail.com",
            },
        )
        self.assertEqual(res.status_code, 201)

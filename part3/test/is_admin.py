import unittest

import requests


class TestAdmin(unittest.TestCase):
    def test_modify_user_same_email(self):
        res = requests.post(
            "http://127.0.0.1:5000/api/v1/auth/login",
            json={"email": "admin@admin.com", "password": "admin"},
        )
        ac = res.json()["access_token"]
        res = requests.post(
            "http://127.0.0.1:5000/api/v1/users/",
            json={
                "first_name": "jhon",
                "last_name": "doe",
                "email": "jhon@doe.org",
                "password": "1234",
            },
            headers={"Authorization": f"Bearer {ac}"},
        )
        uid = res.json()["id"]
        res = requests.put(
            f"http://127.0.0.1:5000/api/v1/users/{uid}",
            json={
                "email": "jhon@doe.org",
            },
            headers={"Authorization": f"Bearer {ac}"},
        )
        self.assertEqual(res.status_code, 400)

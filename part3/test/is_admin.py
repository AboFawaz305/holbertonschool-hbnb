import unittest

import requests

API_URL = "http://127.0.0.1:5000/api/v1/"


class TestAdmin(unittest.TestCase):
    def get_admin_ac(self):
        res = requests.post(
            f"{API_URL}/auth/login",
            json={"email": "admin@admin.com", "password": "admin"},
        )
        return res.json().get("access_token")

    def create_and_login_user(self):
        ac = self.get_admin_ac()
        res = requests.post(
            f"{API_URL}/users/",
            json={
                "first_name": "jhon",
                "last_name": "doe",
                "email": "jhon1@doe.org",
                "password": "p1234",
            },
            headers={"Authorization": f"Bearer {ac}"},
        )
        res = requests.post(
            f"{API_URL}/auth/login",
            json={"email": "jhon1@doe.org", "password": "p1234"},
        )
        ac = res.json()["access_token"]
        return ac

    def test_modify_user_same_email(self):
        ac = self.get_admin_ac()
        res = requests.post(
            f"{API_URL}/users/",
            json={
                "first_name": "jhon",
                "last_name": "doe",
                "email": "jhon@doe.org",
                "password": "p1234",
            },
            headers={"Authorization": f"Bearer {ac}"},
        )
        uid = res.json()["id"]
        res = requests.put(
            f"{API_URL}/users/{uid}",
            json={
                "email": "jhon@doe.org",
            },
            headers={"Authorization": f"Bearer {ac}"},
        )
        self.assertEqual(res.status_code, 400)

    def test_add_amenity_as_admin(self):
        admin_ac = self.get_admin_ac()
        res = requests.post(
            f"{API_URL}/aminities/",
            json={"name": "Wi-Fi 6"},
            headers={"Authorization": f"Bearer {admin_ac}"},
        )
        self.assertEqual(res.status_code, 201)

    def test_add_amenity_not_authorized(self):
        user_ac = self.create_and_login_user()
        res = requests.post(
            f"{API_URL}/aminities/",
            json={"name": "Wi-Fi 6"},
            headers={"Authorization": f"Bearer {user_ac}"},
        )
        self.assertEqual(res.status_code, 403)

    def test_modify_amenity_as_admin(self):
        admin_ac = self.get_admin_ac()
        res = requests.post(
            f"{API_URL}/aminities/",
            json={"name": "Wi-Fi 6"},
            headers={"Authorization": f"Bearer {admin_ac}"},
        )
        aid = res.json()["id"]
        self.assertEqual(res.status_code, 201)
        res = requests.put(
            f"{API_URL}/aminities/{aid}",
            json={"name": "Swimming Pool"},
            headers={"Authorization": f"Bearer {admin_ac}"},
        )
        self.assertEqual(res.status_code, 200)
        res = requests.get(
            f"{API_URL}/aminities/{aid}",
            headers={"Authorization": f"Bearer {admin_ac}"},
        )
        self.assertEqual(res.json()["name"], "Swimming Pool")

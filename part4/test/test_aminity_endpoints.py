import unittest
import requests
from config import DevelopmentConfig


class TestAmenityEndpoint(unittest.TestCase):
    def test_valid_post_amenity(self):
        res = requests.post(
            DevelopmentConfig.API_URL + "/api/v1/aminities", json={"name": "WiFi 6"}
        )
        self.assertEqual(res.status_code, 201)
        res = requests.post(
            DevelopmentConfig.API_URL + "/api/v1/aminities", json={"name": "AC"}
        )
        self.assertEqual(res.status_code, 201)

    def test_invalid_post_amenity(self):
        res = requests.post(DevelopmentConfig.API_URL + "/api/v1/aminities", json={})
        self.assertEqual(res.status_code, 400)

    def test_get_amenity(self):
        res = requests.post(
            DevelopmentConfig.API_URL + "/api/v1/aminities", json={"name": "WiFi 6"}
        )
        self.assertEqual(res.status_code, 201)
        res = requests.post(
            DevelopmentConfig.API_URL + "/api/v1/aminities", json={"name": "AC"}
        )
        self.assertEqual(res.status_code, 201)
        res = requests.get(DevelopmentConfig.API_URL + "/api/v1/aminities")
        json = res.json()
        self.assertEqual(res.status_code, 200)

    def test_get_amenity_by_id(self):
        res = requests.post(
            DevelopmentConfig.API_URL + "/api/v1/aminities", json={"name": "AC"}
        )
        sent_json = res.json()
        self.assertEqual(res.status_code, 201)
        res = requests.get(
            DevelopmentConfig.API_URL + "/api/v1/aminities" + f'/{sent_json["id"]}'
        )
        json = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(sent_json["name"], json["name"])
        self.assertEqual("AC", json["name"])

    def test_put_amenity(self):
        res = requests.post(
            DevelopmentConfig.API_URL + "/api/v1/aminities", json={"name": "AC"}
        )
        sent_json = res.json()
        self.assertEqual(res.status_code, 201)
        res = requests.put(
            DevelopmentConfig.API_URL + "/api/v1/aminities" + f'/{sent_json["id"]}',
            json={"name": "Wi-Fi 6"},
        )
        json = res.json()
        self.assertEqual(res.status_code, 200)
        self.assertEqual("Wi-Fi 6", json["name"])

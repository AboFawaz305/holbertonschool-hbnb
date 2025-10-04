import unittest
import json
import requests
from config import DevelopmentConfig

class TestPlacesEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.place_data = {
            "name": "Test Place",
            "city_id": "123",
            "user_id": "456",
            "description": "A nice place"
        }

    def test_add_place(self):
        response = self.client.post(
            "/api/v1/places",
            data=json.dumps(self.place_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn("id", data)
        self.assertEqual(data["name"], self.place_data["name"])

    def test_add_place_missing_fields(self):
        incomplete_data = {
            "name": "Incomplete Place"
        }
        response = self.client.post(
            "/api/v1/places",
            data=json.dumps(incomplete_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_places(self):
        response = self.client.get("/api/v1/places")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

if __name__ == "__main__":
    unittest.main()
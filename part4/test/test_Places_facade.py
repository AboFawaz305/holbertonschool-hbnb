import unittest

# from app.services import facade
from app.services import HBnBFacade


class testPlacesFacade(unittest.TestCase):

    def setUp(self):
        self.facade = HBnBFacade()

    def test_creat_valid_place(self):

        user_date = {
            "first_name": "aaaaa",
            "last_name": "sssss",
            "email": "aaaa@gmail.com",
        }
        created_user = self.facade.create_user(user_date)
        place_data = {
            "title": "a house",
            "description": "wow house",
            "price": 222,
            "latitude": 10.3423,
            "longitude": 43.4344,
            "owner_id": created_user.id,
        }
        created_place = self.facade.create_place(place_data)

        for key, value in place_data.items():
            self.assertTrue(hasattr(created_place, key))
            self.assertTrue(getattr(created_place, key) == value)
            # for debuging more detail
            # print(f"place.{key} == {value}\\ {getattr(created_place,key) == value}")

    def test_creat_invalid_place(self):

        user_date = {
            "first_name": "aaaaa",
            "last_name": "sssss",
            "email": "aaaa@gmail.com",
        }
        created_user = self.facade.create_user(user_date)
        place_data = {
            "title": "a house",
            "description": "wow house",
            "price": 222,  # cant be 0 or less
            "latitude": 4556,  # should be -90 to 90
            "longitude": -9999,  # sholud be -180 to 180
            "owner_id": created_user.id,
        }
        with self.assertRaises(ValueError):
            created_place = self.facade.create_place(place_data)

    def test_get_place(self):
        user_date = {
            "first_name": "aaaaa",
            "last_name": "sssss",
            "email": "aaaa@gmail.com",
        }
        created_user = self.facade.create_user(user_date)
        place_data1 = {
            "title": "a house",
            "description": "wow house",
            "price": 222,
            "latitude": 10.3423,
            "longitude": 43.4344,
            "owner_id": created_user.id,
        }
        place_data2 = {
            "title": "a house",
            "description": "wow house",
            "price": 222,
            "latitude": 10.3423,
            "longitude": 43.4344,
            "owner_id": created_user.id,
        }
        created_place1 = self.facade.create_place(place_data1)
        created_place2 = self.facade.create_place(place_data2)
        self.assertEqual(created_place1, self.facade.get_place(created_place1.id))
        self.assertNotEqual(created_place1, self.facade.get_place(created_place2.id))

    def test_get_all_places(self):
        user_date = {
            "first_name": "aaaaa",
            "last_name": "sssss",
            "email": "aaaa@gmail.com",
        }
        created_user = self.facade.create_user(user_date)
        place_data1 = {
            "title": "a small house",
            "description": "wow house",
            "price": 222,
            "latitude": 10.3423,
            "longitude": 43.4344,
            "owner_id": created_user.id,
        }
        place_data2 = {
            "title": "a big house",
            "description": "wow house",
            "price": 222,
            "latitude": 10.3423,
            "longitude": 43.4344,
            "owner_id": created_user.id,
        }
        self.facade.create_place(place_data1)
        self.facade.create_place(place_data2)
        all_places = self.facade.get_all_places()
        self.assertEqual(len(all_places), 2)
        self.assertEqual(all_places[0].title, place_data1["title"])

    def test_update_place(self):

        user_date = {
            "first_name": "aaaaa",
            "last_name": "sssss",
            "email": "aaaa@gmail.com",
        }
        created_user = self.facade.create_user(user_date)
        place_data = {
            "title": "a small house",
            "description": "wow house",
            "price": 222,
            "latitude": 10.3423,
            "longitude": 43.4344,
            "owner_id": created_user.id,
        }
        update_data = {
            "title": "a big house",
            "description": "wow house",
            "price": 222,
            "latitude": 10.3423,
            "longitude": 43.4344,
            "owner_id": created_user.id,
        }
        created_place = self.facade.create_place(place_data)
        updated_place = self.facade.update_place(created_place.id, update_data)
        self.assertEqual(updated_place.id, created_place.id)
        self.assertEqual(
            update_data["title"], self.facade.get_place(created_place.id).title
        )
        self.assertEqual(
            updated_place.title, self.facade.get_place(created_place.id).title
        )

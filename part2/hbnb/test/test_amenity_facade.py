import unittest
from app.services import facade
from random import choices, randint
from string import ascii_letters, digits
from app.services import HBnBFacade


class TestAmenityFacade(unittest.TestCase):

    def setUp(self):
        self.facade = HBnBFacade()

    def test_create_valid_amenity(self):
        name = "Wi-Fi 6"
        amenity = {"name": name}
        created_amenity = self.facade.create_amenity(amenity)
        self.assertEqual(created_amenity.name, name)
        self.assertTrue(hasattr(created_amenity, "id"))
        self.assertTrue(hasattr(created_amenity, "created_at"))
        self.assertTrue(hasattr(created_amenity, "updated_at"))

    def test_create_invalid_amenity(self):
        name = "".join(choices(ascii_letters + digits, k=randint(51, 66)))
        amenity = {"name": name}
        with self.assertRaises(ValueError):
            created_amenity = self.facade.create_amenity(amenity)

    def test_get_amenity(self):
        name = "AC"
        amenity = {"name": name}
        ca = self.facade.create_amenity(amenity)
        self.assertEqual(amenity["name"], self.facade.get_amenity(ca.id).name)

    def test_get_all_amenities(self):
        self.assertTrue(len(self.facade.get_all_amenities()) == 0)
        name1 = "Wi-Fi 6"
        amenity = {"name": name1}
        ca1 = self.facade.create_amenity(amenity)
        name2 = "AC"
        amenity = {"name": name2}
        ca2 = self.facade.create_amenity(amenity)
        all_amenities = self.facade.get_all_amenities()
        self.assertTrue(len(all_amenities) == 2)
        self.assertEqual(all_amenities[0].name, name1)
        self.assertEqual(all_amenities[1].name, name2)

    def test_update_amenity(self):
        name = "AC"
        amenity = {"name": name}
        ca = self.facade.create_amenity(amenity)
        name = "Wi-Fi 6"
        new_amenity = {"name": name}
        new_ca = self.facade.update_amenity(ca.id, data=new_amenity)
        self.assertEqual(new_ca.name, self.facade.get_amenity(ca.id).name)

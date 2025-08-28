from app.models import amenity
from app.models.amenity import Amenity
from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from email_validator import validate_email


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        if len(user.first_name) > 50:
            return None
        if len(user.last_name) > 50:
            return None
        try:
            validate_email(user.email)
        except:
            return None
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)


    def create_place(self, place_data):
    # Placeholder for logic to create a place, including validation for price, latitude, and longitude
        owner = self.user_repo.get(place_data["owner_id"])

        if place_data["price"] <= 0:
            raise ValueError("invald price must be bigger then 0")
        if not -90 < place_data["latitude"] < 90:
            raise ValueError("invald latitude must be between -90 to 90")
        if not -180 < place_data["longitude"] < 180:
            raise ValueError("invald longitude must be between -180 to 180")
        if not owner:
            raise ValueError(f"owner needs to be in DB")
        
        del place_data["owner_id"]
        place_data["owner"]= owner

        new_Place = Place(**place_data)
        self.place_repo.add(new_Place)
        return new_Place

    def get_place(self, place_id):
    # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        return self.place_repo.get(place_id)

    def get_all_places(self):
    # Placeholder for logic to retrieve all places
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
    # Placeholder for logic to update a place
        self.place_repo.update(place_id,place_data)
        return self.place_repo.get(place_id)

    def create_amenity(self, amenity):
        if "name" not in amenity.keys():
            raise ValueError("Amenity must have a name")
        if len(amenity["name"]) > 50:
            raise ValueError("Amenity name must not exceed 50 characters.")
        data = Amenity(**amenity)
        self.amenity_repo.add(data)
        return data

    def get_amenity(self, amenity_id) -> Amenity:
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data) -> Amenity:
        self.amenity_repo.update(amenity_id, data)
        return self.get_amenity(amenity_id)

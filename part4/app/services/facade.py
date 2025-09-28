from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository
from email_validator import validate_email


class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    def create_user(self, user_data):
        """
        Verify the user. and store it in the database.
        Return the created user or None if failed
        """

        try:
            user = User(**user_data)
            self.user_repo.add(user)
        except Exception:
            return None
        return user

    def create_admin(self, user):
        user.is_admin = True
        self.user_repo.add(user)

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def create_place(self, place_data):
        """
        Validate a place and store it.
        Return: the created place
        Raise a value error if the data is invalid
        """
        new_place = Place(**place_data)
        self.place_repo.add(new_place)
        return new_place

    def get_place(self, place_id):
        # Placeholder for logic to retrieve a place by ID, including associated owner and amenities
        return self.place_repo.get(place_id)

    def get_all_places(self):
        # Placeholder for logic to retrieve all places
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        # Placeholder for logic to update a place
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)

    def create_aminity(self, amenity):
        if "name" not in amenity.keys():
            raise ValueError("Amenity must have a name")

        data = Amenity(**amenity)
        self.amenity_repo.add(data)
        return data

    def get_aminity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_aminities(self):
        return self.amenity_repo.get_all()

    def update_aminity(self, amenity_id, data):
        self.amenity_repo.update(amenity_id, data)
        return self.get_aminity(amenity_id)

    def create_review(self, review_data):
        """
        Validate a review and store it
        Return the created review
        Raise a ValueError if the review_data is invalid
        """
        new_review = Review(**review_data)
        self.review_repo.add(new_review)
        return new_review

    def get_review(self, review_id):
        if not self.review_repo.get(review_id):
            raise ValueError("the review ID doesn't exist")
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        place = self.get_place(place_id)
        if place is None:
            raise ValueError("place not found")
        return place.reviews

    def update_review(self, review_id, review_data):

        self.review_repo.update(review_id, review_data)
        return self.get_review(review_id)

    def delete_review(self, review_id):

        self.review_repo.delete(review_id)

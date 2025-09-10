from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.user import User
from app.persistence.repository import InMemoryRepository
from email_validator import validate_email


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """
        Verify the user. and store it in the database.
        Return the created user or None if failed
        """
        try:
            user = User(**user_data)
        except Exception:
            return None
        if not 50 > len(user.first_name) > 0:
            return None
        if not 50 > len(user.last_name) > 0:
            return None
        try:
            validate_email(user.email)
        except Exception:
            return None
        similar_emails = [
            email for email in self.get_all_users() if email == user.email
        ]
        if len(similar_emails) > 0:
            # the email is not unique
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
        """
        Validate a place and store it.
        Return: the created place
        Raise a value error if the data is invalid
        """

        if 3 <= len(place_data["title"]) <= 100:
            raise ValueError("invald place title must be between 3 and 100")
        if place_data["price"] <= 0:
            raise ValueError("invald price must be bigger then 0")
        if not -90 <= place_data["latitude"] <= 90:
            raise ValueError("invald latitude must be between -90 to 90")
        if not -180 <= place_data["longitude"] <= 180:
            raise ValueError("invald longitude must be between -180 to 180")
        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError(f"owner needs to be in DB")

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
        if len(amenity["name"]) > 50:
            raise ValueError("Amenity name must not exceed 50 characters.")
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
        if review_data["rating"] not in range(0, 6):
            raise ValueError("rating is not valid ")
        if self.user_repo.get(review_data["user_id"]) is None:
            raise ValueError("user ID does not exist")
        place = self.place_repo.get(review_data["place_id"])
        if place is None:
            raise ValueError("place ID does not exist")
        if place.owner_id == review_data["user_id"]:
            raise ValueError("you cannot review your place")
        new_review = Review(**review_data)
        self.review_repo.add(new_review)
        place.add_review(new_review)
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
        if self.get_place(place_id) == None:
            raise ValueError("place not found")
        place = self.get_place(place_id)
        if place is None:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        if self.review_repo.get(review_id) is None:
            raise ValueError("review id doesn't exist")
        if (
            # if you have to update the rating
            review_data["rating"] is not None
            and review_data["rating"] not in range(0, 6)
        ):
            raise ValueError("rating is not valid ")
        # You can not update the review user and place
        if review_data["user_id"] is not None:
            raise ValueError("You cannot update the user id")
        if review_data["place_id"] is not None:
            raise ValueError("You cannot update the user id")
        self.review_repo.update(review_id, review_data)
        return self.get_review(review_id)

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        review = self.review_repo.get(review_id)
        if review is None:
            raise ValueError("review id doesn't exist")
        place = self.place_repo.get(review.place_id)
        if place is not None:
            place.reviews.remove(review.id)
            self.place_repo.update(place.id, {"reviews": place.reviews})
        self.review_repo.delete(review_id)

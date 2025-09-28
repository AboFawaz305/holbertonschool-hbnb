import json

from app.services import facade
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

api = Namespace("reviews", description="Review operations")

# Define the review model for input validation and documentation
review_model = api.model(
    "Review Post Model",
    {
        "text": fields.String(required=True, description="Text of the review"),
        "rating": fields.Integer(
            required=True, description="Rating of the place (1-5)"
        ),
        "place_id": fields.String(required=True, description="ID of the place"),
    },
)

review_get_model = api.model(
    "Review Get Model",
    {
        "id": fields.String(description="ID of the amenity"),
        "text": fields.String(required=True, description="Text of the review"),
        "rating": fields.Integer(
            required=True, description="Rating of the place (1-5)"
        ),
        "user_id": fields.String(required=True, description="ID of the user"),
        "place_id": fields.String(required=True, description="ID of the place"),
    },
)

review_update_model = api.model(
    "Review Update Model",
    {
        "text": fields.String(description="Text of the review"),
        "rating": fields.Integer(description="Rating of the place (1-5)"),
    },
)


@api.route("/")
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    @api.marshal_with(review_get_model)
    def post(self):
        """Register a new review"""
        user = json.loads(get_jwt_identity())
        review_data = api.payload
        reviewed_place = facade.get_place(review_data["place_id"])
        if reviewed_place is None:
            api.abort(404, "Place not found")
            return
        if user["id"] == reviewed_place["owner_id"]:
            api.abort(400, "invalid data:You cannot review your own place")
        try:
            review_data["user_id"] = user["id"]
            new_review = facade.create_review(review_data)
            return new_review, 200
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, "List of reviews retrieved successfully")
    @api.marshal_list_with(review_get_model)
    def get(self):
        """Retrieve a list of all reviews"""
        return facade.get_all_reviews()


@api.route("/<review_id>")
class ReviewResource(Resource):
    @api.marshal_with(review_get_model)
    @api.response(200, "Review details retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Get review details by ID"""
        try:
            return facade.get_review(review_id)
        except ValueError as e:
            api.abort(404, str(e))

    @jwt_required()
    @api.expect(review_update_model)
    @api.response(200, "Review updated successfully")
    @api.response(404, "Review not found")
    @api.response(400, "Invalid input data")
    @api.marshal_with(review_get_model)
    def put(self, review_id):
        """Update a review's information"""
        user = json.loads(get_jwt_identity())
        review_data = api.payload
        review = facade.get_review(review_id)
        if review is None:
            # Confuse the user so he dont know if the review id exist
            api.abort(403, "Unauthorized action 🚫")
            return
        if not user["id"] == review.user_id:
            api.abort(403, "Unauthorized action")
        try:
            facade.update_review(review_id, review_data)
        except ValueError as e:
            api.abort(400, str(e))

    @jwt_required()
    @api.response(200, "Review deleted successfully")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        """Delete a review"""
        user = json.loads(get_jwt_identity())
        review = facade.get_review(review_id)
        if review is None:
            # Confuse the user so he dont know if the review id exist
            api.abort(403, "Unauthorized action")
            return
        if not user["id"] == review.user_id:
            api.abort(403, "Unauthorized action")
        try:
            facade.delete_review(review_id)
            return {"Review deleted successfully"}, 200
        except ValueError as e:
            api.abort(404, str(e))


@api.route("/places/<place_id>/reviews")
class PlaceReviewList(Resource):
    @api.marshal_list_with(review_get_model)
    @api.response(200, "List of reviews for the place retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        try:
            return facade.get_reviews_by_place(place_id)
        except ValueError as e:
            api.abort(404, str(e))

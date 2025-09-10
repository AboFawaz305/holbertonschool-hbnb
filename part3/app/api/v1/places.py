import json

from app.services import facade
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

api = Namespace("places", description="Place operations")


# Define the models for related entities
amenity_model = api.model(
    "PlaceAmenity",
    {
        "id": fields.String(description="Amenity ID"),
        "name": fields.String(description="Name of the amenity"),
    },
)

user_model = api.model(
    "PlaceUser",
    {
        "id": fields.String(description="User ID"),
        "first_name": fields.String(description="First name of the owner"),
        "last_name": fields.String(description="Last name of the owner"),
        "email": fields.String(description="Email of the owner"),
    },
)

# Define the place model for input validation and documentation
place_create_request_model = api.model(
    "place_create_request_model",
    {
        "title": fields.String(required=True, description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(required=True, description="Price per night"),
        "latitude": fields.Float(required=True, description="Latitude of the place"),
        "longitude": fields.Float(required=True, description="Longitude of the place"),
    },
)

place_create_response_model = api.model(
    "place_create_response_model",
    {
        "id": fields.String(description="id of a place"),
        "title": fields.String(required=True, description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(required=True, description="Price per night"),
        "latitude": fields.Float(required=True, description="Latitude of the place"),
        "longitude": fields.Float(required=True, description="Longitude of the place"),
    },
)


place_model_get_all_places = api.model(
    "place_model_get_all_places",
    {
        "id": fields.String(description="id of a place"),
        "title": fields.String(required=True, description="Title of the place"),
        "latitude": fields.Float(required=True, description="Latitude of the place"),
        "longitude": fields.Float(required=True, description="Longitude of the place"),
    },
)

place_get_response = api.model(
    "place_get_response",
    {
        "id": fields.String(description="id of a place"),
        "title": fields.String(required=True, description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(required=True, description="Price per night"),
        "latitude": fields.Float(required=True, description="Latitude of the place"),
        "longitude": fields.Float(required=True, description="Longitude of the place"),
        "owner": fields.Nested(user_model),
        "amenities": fields.List(fields.String, description="List of amenities ID's"),
    },
)

place_model_put_request = api.model(
    "place_model_put_request",
    {
        "title": fields.String(required=True, description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(required=True, description="Price per night"),
    },
)

# Adding the review model
review_model = api.model(
    "PlaceReview",
    {
        "id": fields.String(description="Review ID"),
        "text": fields.String(description="Text of the review"),
        "rating": fields.Integer(description="Rating of the place (1-5)"),
        "user_id": fields.String(description="ID of the user"),
    },
)

place_model = api.model(
    "Place",
    {
        "title": fields.String(required=True, description="Title of the place"),
        "description": fields.String(description="Description of the place"),
        "price": fields.Float(required=True, description="Price per night"),
        "latitude": fields.Float(required=True, description="Latitude of the place"),
        "longitude": fields.Float(required=True, description="Longitude of the place"),
        "owner_id": fields.String(required=True, description="ID of the owner"),
        "owner": fields.Nested(user_model, description="Owner of the place"),
        "amenities": fields.List(
            fields.Nested(amenity_model), description="List of amenities"
        ),
        "reviews": fields.List(
            fields.Nested(review_model), description="List of reviews"
        ),
    },
)


@api.route("/")
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_create_request_model)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.marshal_with(place_create_response_model)
    def post(self):
        """Register a new place"""
        place_data = api.payload
        user = json.loads(get_jwt_identity())
        try:
            place_data["owner_id"] = user["id"]
            new_place = facade.create_place(place_data)
            return new_place, 200
        except ValueError:
            return {"error": "invalid input data"}, 400

    @api.marshal_list_with(place_model_get_all_places)
    @api.response(200, "List of places retrieved successfully")
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        if places is None:
            places = []
        return


@api.route("/<place_id>")
class PlaceResource(Resource):
    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    @api.marshal_with(place_get_response)
    def get(self, place_id):
        """Get place details by ID"""
        return facade.get_place(place_id)

    @jwt_required()
    @api.response(200, "Place updated successfully")
    @api.response(404, "Place not found")
    @api.response(400, "Invalid input data")
    @api.expect(place_model_put_request)
    def put(self, place_id):
        """Update a place's information"""
        user = json.loads(get_jwt_identity())
        place = facade.get_place(place_id)
        if place is None:
            return {"error": "place not found"}, 404
        if not user["id"] == place.owner_id and  not user['is_admin']:
            return {"error": "Unauthorized action"}, 403
        facade.update_place(place_id, api.payload)
        return {"message": "Place updated successfully"}, 200


from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("amenities", description="Amenity operations")

# Define the amenity model for input validation and documentation
amenity_model = api.model(
    "Amenity",
    {
        "name": fields.String(
            required=True, max_length=50, description="Name of the amenity"
        )
    },
)


@api.route("/")
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new amenity"""
        amenity = api.payload
        try:
            r = facade.create_amenity(amenity)
            return {"name": r.name, "id": r.id}, 201
        except ValueError as e:
            return {"error": "Invalid input"}, 400

    @api.marshal_with(amenity_model)
    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        """Retrieve a list of all amenities"""
        return facade.get_all_amenities(), 200


@api.route("/<amenity_id>")
class AmenityResource(Resource):
    @api.response(200, "Amenity details retrieved successfully")
    @api.response(404, "Amenity not found")
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get amenity details by ID"""
        if facade.get_amenity(amenity_id) is None:
            return {"error": "amenity not found"}, 404
        return facade.get_amenity(amenity_id), 200

    @api.expect(amenity_model)
    @api.response(200, "Amenity updated successfully")
    @api.response(404, "Amenity not found")
    @api.response(400, "Invalid input data")
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity = api.payload
        if facade.get_amenity(amenity_id) is None:
            return {"error": "amenity not found"}, 404
        try:
            r = facade.update_amenity(amenity_id, amenity)
            return {"name": r.name, "id": r.id}, 200
        except ValueError as e:
            return {"error": "Invalid input"}, 400

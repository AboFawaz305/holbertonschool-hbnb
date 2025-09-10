from app.services import facade
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields

api = Namespace("aminities", description="Amenity operations")

aminity_model = api.model(
    "Aminity",
    {
        "name": fields.String(
            required=True, max_length=50, description="Name of the aminity"
        )
    },
)

aminity_get_model = api.model(
    "Aminity",
    {
        "id": fields.String(description="ID of the amenity"),
        "name": fields.String(
            required=True, max_length=50, description="Name of the aminity"
        ),
    },
)


@api.route("/")
class AminityList(Resource):
    @api.expect(aminity_model)
    @api.response(201, "Aminity successfully created")
    @api.response(400, "Invalid input data")
    @api.marshal_with(aminity_get_model)
    def post(self):
        """Register a new aminity"""
        aminity = api.payload
        try:
            amenity = facade.create_aminity(aminity)
            return amenity, 201
        except ValueError:
            return {"error": "Invalid input"}, 400

    @api.marshal_list_with(aminity_get_model)
    @api.response(200, "List of aminities retrieved successfully")
    def get(self):
        """Retrieve a list of all aminities"""
        amenities = facade.get_all_aminities()
        if amenities is None:
            amenities = []
        return amenities, 200


@api.route("/<aminity_id>")
class AmenityResource(Resource):
    @api.response(200, "Aminity details retrieved successfully")
    @api.response(404, "Aminity not found")
    @api.marshal_with(aminity_get_model)
    def get(self, aminity_id):
        """Get amenity details by ID"""
        aminity = facade.get_aminity(aminity_id)
        if aminity is None:
            return {"error": "aminity not found"}, 404
        return aminity, 200

    @api.expect(aminity_model)
    @api.response(200, "Aminity updated successfully")
    @api.response(404, "Aminity not found")
    @api.response(400, "Invalid input data")
    @api.marshal_with(aminity_get_model)
    def put(self, aminity_id):
        """Update an aminity's information"""
        aminity = api.payload
        if facade.get_aminity(aminity_id) is None:
            return {"error": "amenity not found"}, 404
        try:
            aminity = facade.update_aminity(aminity_id, aminity)
            return aminity, 200
        except ValueError:
            return {"error": "Invalid input"}, 400

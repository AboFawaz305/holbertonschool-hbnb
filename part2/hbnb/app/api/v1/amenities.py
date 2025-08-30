from app.services import facade
from flask_restx import Namespace, Resource, fields

api = Namespace("aminities", description="Amenity operations")

# Define the amenity model for input validation and documentation
aminity_model = api.model(
    "Aminity",
    {
        "name": fields.String(
            required=True, max_length=50, description="Name of the aminity"
        )
    },
)


@api.route("/")
class AminityList(Resource):
    @api.expect(aminity_model)
    @api.response(201, "Aminity successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new aminity"""
        aminity = api.payload
        try:
            r = facade.create_aminity(aminity)
            return {"name": r.name, "id": r.id}, 201
        except ValueError as e:
            return {"error": "Invalid input"}, 400

    @api.marshal_with(aminity_model)
    @api.response(200, "List of aminities retrieved successfully")
    def get(self):
        """Retrieve a list of all aminities"""
        amenities = facade.get_all_aminities()
        if amenities == None:
            amenities = []
        return amenities, 200


@api.route("/<aminity_id>")
class AmenityResource(Resource):
    @api.response(200, "Aminity details retrieved successfully")
    @api.response(404, "Aminity not found")
    @api.marshal_with(aminity_model)
    def get(self, aminity_id):
        """Get amenity details by ID"""
        if facade.get_aminity(aminity_id) is None:
            return {"error": "aminity not found"}, 404
        return facade.get_aminity(aminity_id), 200

    @api.expect(aminity_model)
    @api.response(200, "Aminity updated successfully")
    @api.response(404, "Aminity not found")
    @api.response(400, "Invalid input data")
    def put(self, aminity_id):
        """Update an aminity's information"""
        aminity = api.payload
        if facade.get_aminity(aminity_id) is None:
            return {"error": "amenity not found"}, 404
        try:
            r = facade.update_aminity(aminity_id, aminity)
            return {"name": r.name, "id": r.id}, 200
        except ValueError as e:
            return {"error": "Invalid input"}, 400

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model_Create_request = api.model('place_model_Create_request', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(description='owner id'),
})

place_model_Create_responce = api.model('place_model_Create_responce', {
    'id' : fields.String(description='id of a place'),
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(description='owner id'),
})


place_model_get_all_places = api.model('place_model_get_all_places', {
    'id' : fields.String(description='id of a place'),
    'title': fields.String(required=True, description='Title of the place'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
})

place_model_response = api.model('place_model_response', {
    'id' : fields.String(description='id of a place'),
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner': fields.Nested(user_model),
    'amenities': fields.List(fields.String, description="List of amenities ID's")
})

place_model_put_request = api.model('place_model_response', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model_Create_request)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(place_model_Create_responce)
    def post(self):
        """Register a new place"""
        Place_data = api.payload
        try:
            owner_id = Place_data["owner_id"] #scuffed solotion
            new_user = facade.create_place(Place_data)
            new_user.owner_id = owner_id #scuffed solotion
            return  new_user,200
        except ValueError:
            return {"error":"invalid input data"},400

    @api.marshal_list_with(place_model_get_all_places)
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        return facade.get_all_places()

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    @api.marshal_with(place_model_response)
    def get(self, place_id):
        """Get place details by ID"""
        return facade.get_place(place_id)


    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.expect(place_model_put_request)
    def put(self, place_id):
        """Update a place's information"""
        if  facade.get_place(place_id) is None:
            return {"error":"place not found"},404 
        facade.update_place(place_id,api.payload)
        return {"message": "Place updated successfully"},200
        # Placeholder for the logic to update a place by ID
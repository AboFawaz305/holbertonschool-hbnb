import json
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import  get_jwt_identity, jwt_required

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.marshal_with(review_model)
    def post(self):
        """Register a new review"""
        user = json.loads(get_jwt_identity())
        review_data = api.payload
        reviewed_place =facade.get_place(review_data['place_id'])
        if user["id"] == review_model["owner_id"]:
            api.abort(400,"invalid data:You cannot review your own place")
        try:
            new_review =  facade.create_review(review_data)
            return new_review,200
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'List of reviews retrieved successfully')
    @api.marshal_list_with(review_model)
    def get(self):
        """Retrieve a list of all reviews"""
        return facade.get_all_reviews()

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.marshal_with(review_model)
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            return facade.get_review(review_id)
        except ValueError as e:
            api.abort(404,str(e))
    
    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        user = json.loads(get_jwt_identity())
        review_data = api.payload
        if not user['id'] == review_data['user_id']:
            api.abort(403,'Unauthorized action')
        try:
            facade.update_review(review_id,review_data)
        except ValueError as e:
            api.abort(400,str(e))
    
    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        user = json.loads(get_jwt_identity())
        review_data = api.payload
        if not user['id'] == review_data['user_id']:
            api.abort(403,'Unauthorized action')
        try:
            facade.delete_review(review_id)
            return {'Review deleted successfully'}
        except ValueError as e:
            api.abort(404,str(e))
        

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.marshal_list_with(review_model)
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        try:
            return facade.get_reviews_by_place(place_id)
        except ValueError as e:
            api.abort(404,str(e))
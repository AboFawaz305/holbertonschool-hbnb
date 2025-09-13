import json

from app.bcrypt import bcrypt
from app.services import facade
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

api = Namespace("users", description="User operations")

# Define the user model for input validation and documentation
user_model = api.model(
    "User",
    {
        "first_name": fields.String(
            required=True, description="First name of the user"
        ),
        "last_name": fields.String(required=True, description="Last name of the user"),
        "email": fields.String(required=True, description="Email of the user"),
        "password": fields.String(required=True, description="password"),
    },
)

user_model_update = api.model(
    "user_model_update",
    {
        "first_name": fields.String(description="First name of the user"),
        "last_name": fields.String(description="Last name of the user"),
        "email": fields.String(description="Email of the user"),
        "password": fields.String(description="password"),
    },
)


@api.route("/")
class Users(Resource):
    @api.marshal_list_with(user_model)
    @api.response(200, "OK")
    @api.response(404, "Not found")
    def get(self):
        users = facade.get_all_users()
        if not users:
            return [], 200
        return users, 200

    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered")
    @api.response(400, "Invalid input data")
    @jwt_required()
    def post(self):
        user = json.loads(get_jwt_identity())
        if not user["is_admin"]:
            return {"error": "Admin privleges required"}, 403
        user_json = api.payload
        if facade.get_user_by_email(user_json["email"]) is not None:
            return {"error": "Email already registered"}, 400
        new_user = facade.create_user(user_json)
        if new_user is None:
            return {"error": "Invalid input data"}, 400
        return {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
        }, 201


@api.route("/<string:user_id>")
class User(Resource):
    @api.response(200, "OK")
    @api.response(404, "Not found")
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {"error": "Not found"}, 404
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }, 201

    @jwt_required()
    @api.marshal_with(user_model)
    @api.response(200, "OK")
    @api.response(404, "Not found")
    @api.response(400, "Bad Request")
    @api.expect(user_model_update)
    def put(self, user_id):
        user = json.loads(get_jwt_identity())
        if not user["is_admin"]:
            return {"error": "Admin privleges required"}, 403
        user_data = api.payload
        # if not user["id"] == user_id:
        #     api.abort(400, "Bad Request")
        if "email" in user_data.keys():
            similar_emails = [
                u for u in facade.get_all_users() if u.email == user_data["email"]
            ]
            if len(similar_emails) != 0:
                api.abort(400, "email already in use")
        if "password" in user_data.keys():
            user_data["password"] = bcrypt.generate_password_hash(
                user_data["password"]
            ).decode("utf-8")
        facade.user_repo.update(user_id, user_data)
        updated_user = facade.get_user(user_id)
        return updated_user, 200

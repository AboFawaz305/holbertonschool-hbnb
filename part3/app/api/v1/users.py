from app.services import facade
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
        "password":fields.String(required=True,description="password")
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
    def post(self):
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


@api.route("/<string:id>")
class User(Resource):
    @api.response(200, "OK")
    @api.response(404, "Not found")
    def get(self, id):
        user = facade.get_user(id)
        if not user:
            return {"error": "Not found"}, 404
        return {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }, 201

    @api.marshal_with(user_model)
    @api.response(200, "OK")
    @api.response(404, "Not found")
    @api.response(400, "Bad Request")
    def put(self, id):
        user = facade.user_repo.update(id)
        if not user:
            return {"error": "Not found"}, 404
        return user, 200

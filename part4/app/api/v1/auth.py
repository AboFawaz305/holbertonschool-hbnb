from app.services import facade
from flask import json
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

api = Namespace("auth", description="Authentication operations")

login_model = api.model(
    "Login",
    {
        "email": fields.String(required=True, description="User email"),
        "password": fields.String(required=True, description="User password"),
    },
)


@api.route("/login")
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a jwt token"""
        credentials = api.payload
        user = facade.get_user_by_email(credentials["email"])
        if not user or not user.verify_password(credentials["password"]):
            return {"error": "Invalid Credentials"}, 401
        access_token = create_access_token(
            identity=json.dumps({"id": user.id, "is_admin": user.is_admin})
        )
        return {"access_token": access_token}, 200


@api.route("/protected")
class Protected(Resource):
    @jwt_required()
    def get(self):
        """A protected route"""
        current_user = json.loads(get_jwt_identity())
        return {"message": f"Hello, user {current_user['id']}"}, 200

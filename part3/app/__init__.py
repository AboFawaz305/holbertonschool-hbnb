from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restx import Api

from app.api.v1.amenities import api as amenities_ns
from app.api.v1.auth import api as auth_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.users import api as users_ns
from app.bcrypt import bcrypt
from app.db import db
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.user import User

jwt = JWTManager()


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/",
    )

    api.add_namespace(users_ns, "/api/v1/users")
    api.add_namespace(amenities_ns, "/api/v1/aminities")
    api.add_namespace(places_ns, "/api/v1/places")
    api.add_namespace(reviews_ns, "/api/v1/reviews")
    api.add_namespace(auth_ns, "/api/v1/auth")
    with app.app_context():
        db.create_all()

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "User": User,
            "Place": Place,
            "Review": Review,
            "Amenity": Amenity,
        }

    return app

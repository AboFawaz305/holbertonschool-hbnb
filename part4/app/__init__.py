from flask import Flask, app, render_template
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_cors import CORS

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
    app = Flask(__name__)  # , static_url_path="/static")
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

       # Add CORS configuration
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://127.0.0.1:5000", "http://localhost:5000"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/place/<place_id>")
    def place_details(place_id):
        return render_template("place.html")

    @app.route("/place/<place_id>/add-review")
    def add_review(place_id):
        return render_template("add_review.html")

    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/",
        authorizations = {
    'Bearer Auth': { 
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': 'Add "Bearer <your_token_here>"'
    }
}
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

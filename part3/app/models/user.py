from app.bcrypt import bcrypt
from app.db import db
from app.models.BaseModels import BaseModel
from email_validator import validate_email
from sqlalchemy.orm import relationship, validates


class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    places = relationship("Place", backref="owner", lazy=True)
    reviews = relationship("Review", backref="reviewer", lazy=True)

    @validates("password")
    def hash_password(self, key, password):
        """Hash the password before storing it."""
        return bcrypt.generate_password_hash(password).decode("utf-8")

    @validates("email")
    def validate_email(self, key, email):
        try:
            validate_email(email)
        except Exception:
            raise ValueError("Email is invalid")
        similar_emails = self.query.filter(self.email == email).all()
        if len(similar_emails) > 0:
            # the email is not unique
            raise ValueError("Email must be unique")
        return email

    @validates("first_name")
    def validate_first_name(self, key, value):
        if len(value) < 3 or len(value) > 50:
            raise ValueError("First name must be between 3 and 50")
        return value

    @validates("last_name")
    def validate_last_name(self, key, value):
        if len(value) < 3 or len(value) > 50:
            raise ValueError("Last name must be between 3 and 50")
        return value

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"first_name='{self.first_name}', "
            f"last_name='{self.last_name}', "
            f"email='{self.email}', "
            f"is_admin={self.is_admin})>"
        )

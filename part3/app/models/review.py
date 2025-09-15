from app.models.BaseModels import BaseModel
from app.db import db
from sqlalchemy.orm import validates


class Review(BaseModel):
    __tablename__ = "reviews"

    rating = db.Column(db.Integer(), nullable=False)
    text = db.Column(db.String(256), nullable=False)

    @validates("rating")
    def validate_rating(self, key, value):
        if len(value) < 1 or len(value) > 5:
            raise ValueError("Title must be between 3 and 100")
        return value

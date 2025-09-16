from app.db import db
from app.models.BaseModels import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import validates


class Review(BaseModel):
    __tablename__ = "reviews"

    rating = db.Column(db.Integer(), nullable=False)
    text = db.Column(db.String(256), nullable=False)
    reviewer_id = db.Column(db.Integer(), ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.Integer(), ForeignKey("places.id"), nullable=False)

    @validates("rating")
    def validate_rating(self, key, value):
        if value < 1 or value > 5:
            raise ValueError("Rating must be an ineger between 1 and 5")
        return value

    def __repr__(self):
        return (
            f"<Review(id={self.id}, rating={self.rating}, "
            f"reviewer_id={self.reviewer_id}, place_id={self.place_id})>"
        )

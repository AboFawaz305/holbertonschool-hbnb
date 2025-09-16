from app.db import db
from app.models.BaseModels import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship, validates


class PlaceAmenity(BaseModel):
    __tablename__ = "place_amenity"
    place_id = db.Column(db.String(36), ForeignKey("places.id"))
    amenity_id = db.Column(db.String(36), ForeignKey("amenities.id"))


class Place(BaseModel):
    __tablename__ = "places"

    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    owner_id = db.Column(db.Integer(), ForeignKey("users.id"), nullable=False)
    reviews = relationship("Review", backref="place", lazy=True)
    amenities = relationship(
        "Amenity",
        secondary="place_amenity",
        backref=backref("places", lazy=True),
        lazy=True,
    )

    @validates("title")
    def validate_title(self, key, value):
        if len(value) < 3 or len(value) > 100:
            raise ValueError("Title must be between 3 and 100")
        return value

    @validates("price")
    def validate_price(self, key, value):
        if value <= 0:
            raise ValueError("Price must be higher than zero")
        return value

    @validates("latitude")
    def validate_latitude(self, key, value):
        if not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @validates("longitude")
    def validate_longtitude(self, key, value):
        if not -180 <= value <= 180:
            raise ValueError("Longtitude must be between -180 and 180")
        return value

    def __repr__(self):
        return (
            f"<Place(id={self.id}, title='{self.title}', price={self.price}, "
            f"latitude={self.latitude}, longitude={self.longitude}, "
            f"owner_id={self.owner_id})>"
        )

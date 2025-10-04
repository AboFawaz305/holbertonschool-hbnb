from app.db import db
from app.models.BaseModels import BaseModel
from sqlalchemy.orm import validates


class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False, unique=True)

    @validates("name")
    def validate_name(self, key, value):
        if len(value) < 3 or len(value) > 50:
            raise ValueError("name must be between 3 and 50")
        return value

    def __repr__(self):
        return f"<Amenity(id={self.id}, name='{self.name}')>"

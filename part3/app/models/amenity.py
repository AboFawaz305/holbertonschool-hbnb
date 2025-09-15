from app.models.BaseModels import BaseModel
from app.db import db
from sqlalchemy.orm import validates


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    __tablename__ = "aminities"

    name = db.Column(db.String(50), nullable=False, unique=True)

    @validates("name")
    def validate_name(self, key, value):
        if value < 3 or value > 50:
            raise ValueError("name must be between 3 and 50")
        return value

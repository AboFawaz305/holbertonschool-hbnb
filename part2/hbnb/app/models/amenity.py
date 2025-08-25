from app.models.BaseModel import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        self.super().__init__()
        self.name = name
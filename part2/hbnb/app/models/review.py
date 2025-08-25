from app.models.BaseModel import BaseModel


class Review(BaseModel):
    def __init__(self, rating , place , user):
        self.super().__init__()
        self.rating = ratin
        self.place = place
        self.user = user
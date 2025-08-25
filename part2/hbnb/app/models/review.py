from app.models.BaseModels import BaseModel


class Review(BaseModel):
    def __init__(self, rating, text, place, user):
        super().__init__()
        self.rating = rating
        self.text = text
        self.place = place
        self.user = user

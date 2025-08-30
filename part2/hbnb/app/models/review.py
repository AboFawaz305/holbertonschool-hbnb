from app.models.BaseModels import BaseModel


class Review(BaseModel):
    def __init__(self, rating, text, place_id, user_id):
        super().__init__()
        self.rating = rating
        self.text = text
        self.place_id = place_id
        self.user_id = user_id

import uuid
from datetime import datetime
from app.db import db


class BaseModel(db.Model):
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel
    __utc_now = lambda: datetime.now()
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=__utc_now)
    updated_at = db.Column(db.DateTime, default=__utc_now, onupdate=__utc_now)

    # def save(self):
    #    """Update the updated_at timestamp whenever the object is modified"""
    #    self.updated_at = datetime.now()

    # def update(self, data):
    #    """Update the attributes of the object based on the provided dictionary"""
    #    for key, value in data.items():
    #        if hasattr(self, key):
    #            setattr(self, key, value)
    #    self.save()  # Update the updated_at timestamp

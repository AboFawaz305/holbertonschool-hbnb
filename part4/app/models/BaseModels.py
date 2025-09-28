import uuid
from datetime import datetime, timezone

from app.db import db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(
        db.String(36),
        primary_key=True,
        # Use a UUID
        default=lambda: str(uuid.uuid4()),
    )
    created_at = db.Column(
        db.DateTime,
        # Use utc time
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at = db.Column(
        db.DateTime,
        # Use utc
        default=lambda: datetime.now(timezone.utc),
        onupdate=datetime.now,
    )

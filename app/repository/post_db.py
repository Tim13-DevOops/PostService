from datetime import datetime
from .database import db
from dataclasses import dataclass


@dataclass
class Post(db.Model):
    id: int
    timestamp: datetime
    description: str
    deleted: bool
    image: str
    profile_username: str

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    description = db.Column(db.String(1000))
    deleted = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(255))
    profile_username = db.Column(db.String(255))

    def __repr__(self):
        return f"Product {self.name}"
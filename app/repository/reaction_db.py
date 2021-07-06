from datetime import datetime
from .database import db
from dataclasses import dataclass


@dataclass
class Reaction(db.Model):
    id: int
    timestamp: datetime
    like: bool
    post_id: int
    profile_username: str

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    like = db.Column(db.Boolean, default=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    profile_username = db.Column(db.String(255))

    def __repr__(self):
        return f"Reaction {self.like}"

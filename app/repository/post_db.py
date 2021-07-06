from datetime import datetime
from .database import db
from dataclasses import dataclass


@dataclass
class Post(db.Model):
    id: int
    description: str
    deleted: bool
    image: str
    profile_username: str
    timestamp: datetime
    likes: int = 0
    dislikes: int = 0
    liked_by_user: bool = False
    disliked_by_user: bool = False

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    description = db.Column(db.String(1000))
    deleted = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(255))
    profile_username = db.Column(db.String(255))
    reactions = db.relationship("Reaction", backref="post", lazy=True)

    def __repr__(self):
        return f"Post {self.name}"

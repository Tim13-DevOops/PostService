from datetime import datetime
from .database import db
from dataclasses import dataclass


@dataclass
class Tag(db.Model):
    id: int
    timestamp: datetime
    text: str
    post_id: int

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    text = db.Column(db.String(255), default=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)

    def __repr__(self):
        return f"Tag {self.text}"

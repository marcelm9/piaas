from datetime import datetime
from .extensions import db


class Observation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    animal_name = db.Column(db.String(100), nullable=False)
    stream_name = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

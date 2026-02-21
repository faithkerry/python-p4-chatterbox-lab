from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column, Integer, String, DateTime
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

# Naming convention for migrations
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String, nullable=False)              # Message text
    username = db.Column(db.String, nullable=False)          # Author of the message
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Optional: fields to serialize automatically
    serialize_rules = ('-created_at', '-updated_at')  # example, adjust if needed

    def __repr__(self):
        return f"<Message id={self.id} username={self.username} body={self.body[:20]}>"
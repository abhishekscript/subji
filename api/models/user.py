from api import db
from sqlalchemy.sql import func

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    createdAt = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updatedAt = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class UserSerializer:
    def __init__(self, userObject):
        self.ALLOWED_FIELDS = User.__table__.columns.keys()
        self.userObject     = userObject

    def get(self):
        fields = {}
        for field in self.ALLOWED_FIELDS:
            fields[field] = eval("self.userObject."+field)
        return fields
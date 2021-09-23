from api import db
from sqlalchemy.sql import func

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    username = db.Column(db.String, unique=True, nullable=False)
    createdAt = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updatedAt = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class UserSerializer:
    def __init__(self, userObject):
        if not userObject:
            self.view = None
        else:
            self.view = { 
            "id" : userObject.id ,
            "username"  : userObject.username,
            "createdAt" : userObject.createdAt, 
            "updatedAt" : userObject.updatedAt
            }
        

from .user import User
from api import db
from sqlalchemy.sql import func


class Plan:
    def __init__(self):
        self.map = {
            "FREE"    : [0,    0.0],
            "TRIAL"   : [7,    0.0],
            "LITE_1M" : [30,  100.0],
            "PRO_1M"  : [30,  200.0],
            "LITE_6M" : [180, 500.0],
            "PRO_6M"  : [180, 900.0]
        }

class PlanSubScription(db.Model):
    id        = db.Column(db.Integer, primary_key=True, auto_increment=True)
    plan      = db.Column(db.String, nullable= False)
    userId    = db.Column( db.ForeignKey(User.id))
    startDate = db.Column(db.DateTime(timezone=True), nullable=False)
    endDate   = db.Column(db.DateTime(timezone=True), nullable=False)
    createdAt = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updatedAt = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PlanSubScriptionSerializer:
    def __init__(self, planObject):
        self.view = {
            "plan"      : planObject.plan,
            "userId"    : planObject.userId,
            "startDate" : planObject.startDate,
            "endDate"   : planObject.endDate,
            "createdAt" : planObject.createdAt,
            "updatedAt" : planObject.updatedAt
        }
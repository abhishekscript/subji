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
    id        = db.Column(db.Integer, primary_key=True)
    plan      = db.Column(db.String, nullable= False)
    userId    = db.Column(db.ForeignKey(User.id))
    status    = db.Column(db.Boolean, nullable=False, default=True)
    startDate = db.Column(db.DateTime(timezone=True), nullable=False)
    endDate   = db.Column(db.DateTime(timezone=True), nullable=False)
    createdAt = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updatedAt = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Order(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    plan = db.Column(db.String, nullable= False)
    userId  = db.Column(db.ForeignKey(User.id))
    status  = db.Column(db.String, nullable=False)
    paymentId = db.Column(db.String, nullable=True)
    createdAt = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updatedAt = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PlanSubScriptionSerializer:
    def __init__(self, planObject):
        self.ALLOWED_FIELDS = PlanSubScription.__table__.columns.keys()
        self.planObject     = planObject

    def get(self):
        fields = {}
        for field in self.ALLOWED_FIELDS:
            fields[field] = eval("self.planObject."+field)
        return fields


class OrderSerializer:
    def __init__(self, orderObject):
        self.ALLOWED_FIELDS = Order.__table__.columns.keys()
        self.orderObject     = orderObject

    def get(self):
        fields = {}
        for field in self.ALLOWED_FIELDS:
            fields[field] = eval("self.orderObject."+field)
        return fields
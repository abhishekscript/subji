from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///subji.sqlite"
db = SQLAlchemy(app)

from api import userView, subscriptionView

db.create_all()

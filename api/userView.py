
from api import app,db,jsonify
from .models.user import User, UserSerializer
from sqlalchemy import exc
import json

@app.route('/user/<name>', methods = ['PUT'])
def addUser(name):
    try:
        obj = User(username=name)
        db.session.add(obj)
        db.session.commit()
        return jsonify({"message" : "Added User"}), 200

    except exc.SQLAlchemyError as e:
        return jsonify({"message" : "Failed To Add User" , "err" : str(e)  }), 409

@app.route("/user", methods = ["GET"] )
def getUsers():
    # Serialize query objects
    d=[ UserSerializer(u).view for u in db.session.query(User).all() ]
    return jsonify(d)


@app.route("/user/<name>", methods = ["GET"])
def getUserByName( name ):

    userData = db.session.query(User).filter(User.username==name).first()
    userData = UserSerializer(userData)
    if userData.view!= None:
        return jsonify(userData.view)
    
    return jsonify({"message" : "user does not exist" }), 204


'''
@app.route("/user/<int:userid>", methods = ["GET"])
def getUserById( userid ):

    userData = db.session.query(User).get(int(userid))
    userData = UserSerializer(userData)
    if userData.view!= None:
        return jsonify(userData.view)
    
    return jsonify({"message" : "user does not exist" }), 204
'''
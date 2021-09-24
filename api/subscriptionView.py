
from api import app,db,jsonify, request
from datetime import datetime, timedelta
from .models.subscription import Plan, PlanSubScription
from .models.user import User, UserSerializer
from sqlalchemy import exc,desc
import json


def getExistingSubscription( userid ):
    records = db.session.query(PlanSubScription).join(User).filter( User.id == userid ).order_by(desc(PlanSubScription.createdAt)).all()
    for record in records:
        print("rec", record)
    return records
    
@app.route('/subscription', methods = ['POST'])
def addSubscription():
    inputData = request.get_json()
    name = inputData['user_name']
    userData = db.session.query(User).filter(User.username==name).first()
    userData = UserSerializer(userData)
    if userData.view!=None:
        
        planId  = inputData.get('plan_id')
        planMap = Plan().map
        if planId not in planMap:
            return jsonify({"message" : "Invalid Plan"})
        startDate = datetime.strptime( inputData['start_date'], "%Y-%m-%d")
        endDate   = None   # fetch day
        if endDate == 0:
            endDate = startDate + timedelta(days = 36500)
        else:
            endDate = startDate + timedelta(days = planMap[planId][0])
        
        subs = getExistingSubscription( userData.view['id'] )
        if subs==None:
            planSub = PlanSubScription( plan= planId, userId= userData.view['id'] , startDate= startDate, endDate= endDate )
            db.session.add(planSub)
            db.session.commit()
            return jsonify({})
        else:
            return jsonify({"message" : "Plan already exists" })
    else:
        return jsonify({"message" :  "User does not exist" })


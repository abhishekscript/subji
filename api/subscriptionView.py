
import json, dateparser
from sqlalchemy import exc,desc
from api import app,db,jsonify, request
from datetime import date, datetime, timedelta
from .services.payment import PaymentGateway
from .models.user import User, UserSerializer
from .models.subscription import Plan, Order, PlanSubScription, PlanSubScriptionSerializer

@app.route("/plan", methods = ['GET'])
def getPlans():
    return Plan().map



def getExistingSubscription( username ):
    record = db.session.query(PlanSubScription).join(User).filter( 
        User.username == username, PlanSubScription.status == True ).order_by(
        desc(PlanSubScription.createdAt)
    ).first()

    if record!=None:
        
        planSubscribed = PlanSubScriptionSerializer(record).get()
        print(planSubscribed)
        return planSubscribed
    return None



def buyPlanSubscription( subs, plan_id, name ):
    plans = Plan().map
    currentPlan    = plans[ subs['plan'] ]
    requestedPlan  = plans[ plan_id ]
    payload = {
        "user_name" : name,
        "payment_type" : "DEBIT" if currentPlan[1] < requestedPlan[1] else "CREDIT",
        "amount" : requestedPlan[1]
    }
    payInfo = PaymentGateway().post(payload)
    return payInfo, payload


@app.route('/subscription', methods = ['POST'])
def addSubscription():
    inputData = request.get_json()
    name = inputData['user_name']
    userData = db.session.query(User).filter(User.username==name).first()
    userData = UserSerializer(userData).get()
    planId   = inputData['plan_id']
    planMap    = Plan().map
    requestedPlan = planMap[ planId ]
    startDate = datetime.strptime( inputData['start_date'], "%Y-%m-%d")
    endDate   = None
    if userData=={}:
        return jsonify({"message" : "User does not exist"})
    
    lastActivePlan = getExistingSubscription( name )
    if lastActivePlan!=None and lastActivePlan['plan'] == planId:
        return jsonify({"message" : "plan already subscribed"})
    
    amount = requestedPlan[1]
    paymentId = None
    if requestedPlan[0] == 0:
            endDate = startDate + timedelta(days=36500)
    else:
            endDate = startDate + timedelta(days = planMap[planId][0])
            payInfo ={}
            if lastActivePlan==None:
                payInfo,payload = buyPlanSubscription({"plan":"FREE"}, planId, name)
            else:
                payInfo,payload = buyPlanSubscription(lastActivePlan, planId, name)
            
            if payInfo.status_code == 200:
                
                amount = -amount if payload["payment_type"] == 'CREDIT' else amount

                paymentId = payInfo.json()['payment_id']
                if lastActivePlan:
                    db.session.query(PlanSubScription).filter_by(id = lastActivePlan['id']).update({ "status" : False })
            else:
                return jsonify({"message" : "could not subscribe to the plan "})

    planSub = PlanSubScription( plan= planId, userId= userData['id'] , startDate= startDate, endDate= endDate )
    db.session.add(planSub)
    orderObj = Order(plan=planId, userId=userData['id'], status='SUCCESS', paymentId = paymentId)
    db.session.add(orderObj)
    db.session.commit()

    return jsonify({"status" : "success", "amount" :  amount    })


@app.route("/subscription/<username>")
@app.route("/subscription/<username>/<currentDate>")
def userSubscription(username, currentDate=None):
    
    if username and currentDate:
            currentSub  = getExistingSubscription(username)
            currentDate = dateparser.parse(currentDate)
            leftDays    = currentSub['endDate'] - currentDate
            return jsonify({"plan_id" : currentSub['plan'] , "days_left" : leftDays.days })

    else:
        records = db.session.query(PlanSubScription).join(User).filter( 
            User.username == username,
        ).all()
        
        return jsonify([ PlanSubScriptionSerializer(record).get() for record in records ])
        
    
    #db.session.query(PlanSubScription).
    return jsonify({"message" : "received only username"})
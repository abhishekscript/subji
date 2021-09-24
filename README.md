# subji
Low Level Design for subji

#Code Structure :
```
  api
   |__init.py   #contains app config and route imports
   |__models        # contains all models & entity serializers
   |_____ user.py   # user model
   |_____ subscription.py    # subscription and plan entities
   |__services
   |_____ payment.py    # payment gateway service integration
   |__userView.py
   |__subscriptionView.py
   main.py   # main server file
```

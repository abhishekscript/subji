import json, requests

class PaymentGateway:
	def __init__(self):
		self.url = "https://dummy-payment-server.herokuapp.com/payment"

	def post(self, payload):
		payload  = json.dumps(payload)
		headers  = {"Content-Type":"application/json"}
		response = requests.request("POST", self.url, headers=headers, data=payload)
		return response

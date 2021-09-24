import requests

url = "https://dummy-payment-server.herokuapp.com/payment"


def pay(payload):
    payload = payload
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return response
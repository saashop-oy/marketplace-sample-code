import os
import json
import requests
import uuid
import base64

_API_STAGE = os.getenv('API_STAGE', "")
_API_VERSION = os.getenv('API_VERSION', "")
_CLIENT_ID = os.getenv('CLIENT_ID', "")
_CLIENT_SECRET = os.getenv('CLIENT_SECRET', "")
_INTERNAL_ERROR_CODE = 500
_TOKEN=""

def base64wrapper(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

"""
This endpoint can be used to authenticate and crate token."""
def createToken():
    try:
        endpoint = f'https://{_API_STAGE}/auth/{_API_VERSION}/tokens'
        headers = {
            "X-Request-ID": str(uuid.uuid4()),
            "Authorization": 'Basic ' + base64wrapper(f'{_CLIENT_ID}:{_CLIENT_SECRET}')
        }
        response = requests.post(endpoint, headers=headers, data={})
        return response.json(), response.status_code
    except Exception as e:
        print(f'{e}')
        return e, _INTERNAL_ERROR_CODE


"""
Retrieve an order.
Order includes details about the buyer and the purchased product. Each order is identified by an identifier orderId."""
def getOrder(orderId):
    try:
        endpoint = f'https://{_API_STAGE}/lead/{_API_VERSION}/orders/{orderId}'
        headers = {
            "X-Request-ID": str(uuid.uuid4()),
            "Authorization": _TOKEN
        }
        response = requests.get(endpoint, headers=headers)
        return response.json(), response.status_code
    except Exception as e:
        print(f'{e}')
        return e, _INTERNAL_ERROR_CODE


# Code
token, status = createToken()
if status != 201:
    print(f'ERROR: API call failed. {status}, {token}')
    exit()

# The orderId cames from marketplaceEvent.
orderId = '3e6e133b-a2ab-4e36-8b0f-38a24c085ce6'

_TOKEN = token.get("tokenType", "") + " " + token.get("accessToken", "")
order, status = getOrder(orderId=orderId)
if status != 200:
    print(f'ERROR: API call failed. {status}, {order}')
    exit()

print(order)
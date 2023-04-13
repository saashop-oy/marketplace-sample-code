import os
import json
import requests
import uuid
import base64


"""
    Source env.rc to export some sensitive data to Environment Variables.
    Get these Variable here.
"""
_API_STAGE = os.getenv('API_STAGE', "")
_API_VERSION = os.getenv('API_VERSION', "")
_CLIENT_ID = os.getenv('CLIENT_ID', "")
_CLIENT_SECRET = os.getenv('CLIENT_SECRET', "")
INTERNAL_ERROR_CODE = 500

def base64wrapper(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

"""
    Call checkAPIstatus to see the simple ping response form API server.
"""
def checkAPIStatus():
    try:
        endpoint = f'https://{_API_STAGE}/base/{_API_VERSION}/ping'
        response = requests.get(endpoint)
        return response.json(), response.status_code
    except Exception as e:
        print(f'{e}')
        return e, INTERNAL_ERROR_CODE

"""
    pass ClientId and ClientSecret to this method and get time-limited JWT Bearer token.
    Token will be expired in 30 minutes.
"""
def authenticate():
    try:
        endpoint = f'https://{_API_STAGE}/auth/{_API_VERSION}/tokens'
        headers = {
            "X-Request-ID": str(uuid.uuid4()),
            "Authorization": 'Basic ' + base64wrapper(f'{_CLIENT_ID}:{_CLIENT_SECRET}')
        }
        response = requests.post(endpoint, headers=headers, data={})
        if response.status_code == 201:
            return response.json().get("tokenType", "") + " " + response.json().get("accessToken", ""), response.status_code
        return response.json(), response.status_code
    except Exception as e:
        print(f'{e}')
        return e, INTERNAL_ERROR_CODE


"""
    Get chunk of marketplaceEvents.
    - limit: indicate the amount of data retrieves. recommended value is 50
    return value is an array of new added marketplaceEvents with maximum size of "limit".
"""
def getMarketplaceEvents(token, url, limit):
    marketplaceEvents = []
    hasMore = True
    try:
        while (hasMore):
            params = {
                "limit": limit
            }
            headers = {
                "X-Request-ID": str(uuid.uuid4()),
                "Authorization": token
            }
            print(f'Invoke API: {url}/?limit={limit}')
            response = requests.get(url, params=params, headers=headers)
            for marketplaceEvent in response.json().get("marketplaceEvents", []):
                marketplaceEvents.append(marketplaceEvent)
            hasMore = response.json().get("hasMore", False)
        return marketplaceEvents, response.status_code
    except Exception as e:
        print(f'{e}')
        return e, INTERNAL_ERROR_CODE


"""
    Get order by it's Id.    
    - orderId
    return value is an Order object.
"""
def getOrder(token, orderId):
    try:
        endpoint = f'https://{_API_STAGE}/lead/{_API_VERSION}/orders/{orderId}'
        headers = {
            "X-Request-ID": str(uuid.uuid4()),
            "Authorization": token
        }
        print(f'Invoke API: {endpoint}')
        response = requests.get(endpoint, headers=headers)
        orderObj = response.json()
        # Add Your code here
        return orderObj, response.status_code
    except Exception as e:
        print(f'{e}')
        return e, INTERNAL_ERROR_CODE


"""
License includes details about the buyer and the purchased product. Each license is identified by an identifier licenseId.
"""
def getLicense(token, licenseId):
    try:
        endpoint = f'https://{_API_STAGE}/lead/{_API_VERSION}/licenses/{licenseId}'
        headers = {
            "X-Request-ID": str(uuid.uuid4()),
            "Authorization": token
        }
        print(f'Invoke API: {endpoint}')
        response = requests.get(endpoint, headers=headers)
        licenseObj = response.json()
        # Add Your code here
        return licenseObj, response.status_code
    except Exception as e:
        print(f'{e}')
        return e, INTERNAL_ERROR_CODE

def dispatch(token, marketplaceEvent):
    additionalProperties = marketplaceEvent.get("additionalProperties", [])
    for additionalProperty in additionalProperties:
        if (additionalProperty.get("name", "") == "orderId"):
            return getOrder(token, additionalProperty.get("value", ""))
        elif (additionalProperty.get("name", "") == "licenseId"):
            return getLicense(token, additionalProperty.get("value", ""))

# checkAPIStatus
ping, status = checkAPIStatus()
if status != 200:
    print('ERROR: API call failed.')
    exit()
#print(ping)

# authenticate
token, status = authenticate()
if status != 201:
    print(f'ERROR: API call failed. {status}, {token}')
    exit()
#print(token)

# getMarketplaceEvents
marketplaceEvents, status = getMarketplaceEvents(
        token,
        f'https://{_API_STAGE}/lead/{_API_VERSION}/marketplaceEvents', 40)
if status != 200:
    print(f'ERROR: API call failed. {status}')
    exit()
#print(marketplaceEvents)
for marketplaceEvent in marketplaceEvents:
    dispatch(token, marketplaceEvent)

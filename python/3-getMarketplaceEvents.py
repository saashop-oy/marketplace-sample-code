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
Retrieve new MarketplaceEvents which includes links to orders and licences."""
def getMarketplaceEvents(offset=0, limit=50):
    try:
        endpoint = f'https://{_API_STAGE}/lead/{_API_VERSION}/marketplaceEvents'
        params = {
            "offset": offset,
            "limit": limit
        }
        headers = {
            "X-Request-ID": str(uuid.uuid4()),
            "Authorization": _TOKEN
        }
        response = requests.get(endpoint, params=params, headers=headers)
        return response.json(), response.status_code
    except Exception as e:
        print(f'{e}')
        return e, _INTERNAL_ERROR_CODE


# Code
token, status = createToken()
if status != 201:
    print(f'ERROR: API call failed. {status}, {token}')
    exit()

_TOKEN = token.get("tokenType", "") + " " + token.get("accessToken", "")
marketplaceEvents, status = getMarketplaceEvents(offset=0, limit=50)
if status != 200:
    print(f'ERROR: API call failed. {status}, {marketplaceEvents}')
    exit()

print(marketplaceEvents)
# marketplaceEvents should be Empty or below object. If it's Empty you have nothing to do.
# If not empty, you have to use value of orderId to fetch Order in next API.
"""
{
  "hasMore": false,
  "marketplaceEvents": [
    {
      "additionalProperties": [
        {
          "description": "Unique identifier of the order. This identifer can be used to fetch the order.",
          "name": "orderId",
          "value": "3e6e133b-a2ab-4e36-8b0f-38a24c085ce6"
        }
      ],
      "description": "Provisioning has been started",
      "detailedDescription": "Provisioning has been started",
      "eventId": "3c17a28c-819f-45c9-af01-dfec33cd4a45",
      "eventTime": "2023-03-28T11:49:57.557066+00:00",
      "eventTypeCode": "ServicePurchased",
      "seenTime": null,
      "sellerId": "5",
      "statusCode": "ProvisioningStarted"
    },
    {
      "additionalProperties": [
        {
          "description": "Unique identifier of the order. This identifer can be used to fetch the order.",
          "name": "orderId",
          "value": "0b31fe86-b5f6-4b4d-818e-c4896b4c20e8"
        }
      ],
      "description": "Provisioning has been started",
      "detailedDescription": "Provisioning has been started",
      "eventId": "6c2e4a76-6163-4cdc-a798-d591e8fd0b21",
      "eventTime": "2023-03-28T11:49:59.314374+00:00",
      "eventTypeCode": "ServicePurchased",
      "seenTime": null,
      "sellerId": "5",
      "statusCode": "ProvisioningStarted"
    }
  ]
}
"""
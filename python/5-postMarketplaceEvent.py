import os
import json
import requests
import uuid
import base64
import json


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
You can send a MarketplaceEvent. MarketplaceEvent is sent to inform the progress of the service provisioning."""
def postMarketplaceEvents(body):
    try:
        endpoint = f'https://{_API_STAGE}/lead/{_API_VERSION}/marketplaceEvents'        
        headers = {
            "Content-Type": "application/json",
            "X-Request-ID": str(uuid.uuid4()),
            "Authorization": _TOKEN
        }
        response = requests.post(endpoint, headers=headers, data=body)
        return response.status_code
    except Exception as e:
        print(f'{e}')
        return _INTERNAL_ERROR_CODE


# Code
token, status = createToken()
if status != 201:
    print(f'ERROR: API call failed. {status}, {token}')
    exit()

_TOKEN = token.get("tokenType", "") + " " + token.get("accessToken", "")

# Id of order you want to add marketplaceEvent.
orderId = '3e6e133b-a2ab-4e36-8b0f-38a24c085ce6'

# eventTypeCode, required, string
# Enum: "ServicePurchased" "Evaluation" "Trial" "UpgradeToTrial" "UpgradeToPurchase" 
# Currently supported types: ServicePurchased
eventTypeCode = 'ServicePurchased'

# statusCode, required, string
# Enum: "ProvisioningStarted" "ProvisioningInProgress" "ProvisioningCompleted" "ProvisioningFailed"
statusCode = 'ProvisioningInProgress'

# description, required, string
Description = 'Provisioning has been started'

marketplaceEvent = {
  "additionalProperties": [
    {
      "description": "Unique identifier of the order. This identifer can be used to fetch the order.",
      "name": "orderId",
      "value": orderId
    }
  ],
  "description": Description,
  "eventTypeCode": eventTypeCode,
  "statusCode": statusCode
}
status = postMarketplaceEvents(json.dumps(marketplaceEvent))
if status != 201:
    print(f'ERROR: API call failed. {status}')
    exit()

print ('marketplaceEvent posted!')
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

def base64wrapper(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    return base64_message

"""
This ping endpoint can be used to authenticate and crate token.
"""
def createToken():
    try:
        endpoint = f'https://{_API_STAGE}/auth/{_API_VERSION}/tokens'
        headers = {
            "X-Request-ID": str(uuid.uuid4()),
            "Authorization": f'Basic ' + base64wrapper(f'{_CLIENT_ID}:{_CLIENT_SECRET}')
        }
        response = requests.post(endpoint, headers=headers, data={})
        return response.json(), response.status_code
    except Exception as e:
        print(f'{e}')
        return e, _INTERNAL_ERROR_CODE

# Code
token, status = createToken()
if status != 200:
    print(f'ERROR: API call failed. {status}, {token}')
else:
    print(token)

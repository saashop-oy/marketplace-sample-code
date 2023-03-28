import os
import json
import requests

_API_STAGE = os.getenv('API_STAGE', "")
_API_VERSION = os.getenv('API_VERSION', "")
_INTERNAL_ERROR_CODE = 500

"""
This ping endpoint can be used to check the status of the API without any authentication headers.
"""
def checkAPIStatus():
    try:
        endpoint = f'https://{_API_STAGE}/base/{_API_VERSION}/ping'
        response = requests.get(endpoint)
        return response.json(), response.status_code
    except Exception as e:
        print(f'{e}')
        return e, _INTERNAL_ERROR_CODE

# Code
ping, status = checkAPIStatus()
if status != 200:
    print('ERROR: API call failed.')
else:
    print(ping)
"""
Script used to run smoke tests
"""
import requests
import json
from datetime import datetime, timedelta

SMOKE_TEST_RUNNING = False
URL = "http://localhost/auth/realms/safe-zone/protocol/openid-connect/token"
HEADERS = {
  'Content-Type': 'application/x-www-form-urlencoded'
}
payload='grant_type=password&client_id=safe-zone&username=Tester&password=cmpt371'
response = requests.request("POST", URL, headers=HEADERS, data=payload)
# returns object containing these keys:
# access_token, expires_in, refresh_expires_in, refresh_token, token_type, not-before-policy, session_state, scope

token = json.loads(response.text)["access_token"]
token_lifespan = json.loads(response.text)["expires_in"]
refresh_token = json.loads(response.text)["refresh_token"]
current_time = datetime.utcnow()
token_expiration_time = current_time + timedelta(seconds=int(token_lifespan))


print(token_lifespan)
#clientid, grant type, refreshtoken

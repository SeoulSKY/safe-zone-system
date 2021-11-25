"""
Script used to run smoke tests
"""
import requests
import json
import unittest
from datetime import datetime, timedelta

SMOKE_TEST_RUNNING = False
OAUTH_URL = "http://localhost/auth/realms/safe-zone/protocol/openid-connect/token"
OAUTH_HEADERS = {
  'Content-Type': 'application/x-www-form-urlencoded'
}
OAUTH_PAYLOAD = 'grant_type=password&client_id=safe-zone&username=testaccount&password=abcd1234'
response = requests.request("POST", OAUTH_URL, headers=OAUTH_HEADERS, data=OAUTH_PAYLOAD)
# returns object containing these keys:
# access_token, expires_in, refresh_expires_in, refresh_token, token_type, not-before-policy, session_state, scope
access_token = json.loads(response.text)["access_token"]
token_lifespan = json.loads(response.text)["expires_in"]
refresh_token = json.loads(response.text)["refresh_token"]
current_time = datetime.utcnow()
token_expiration_time = current_time + timedelta(seconds=int(token_lifespan))

oauth_token = "Bearer " + access_token

######### MIBS SMOKE TEST #########
mibs_url = "http://localhost/mibs/hello"
mibs_headers = {"Authorization": oauth_token}
mibs_response = requests.request("GET", mibs_url, headers=mibs_headers, data={})

class TestMIBsSmokeTest(unittest.TestCase):
  def test_response_text(self):
    print("Mibs Smoke Test")
    self.assertEqual(mibs_response.text, "Hello from MIBS")


######### CMS SMOKE TEST #########
cms_url = "http://localhost/cms/hello"
cms_response = requests.request("GET", cms_url, headers={}, data={})

class TestCMSSmokeTest(unittest.TestCase):
  def test_response_text(self):
    print("CMS Smoke Test")
    self.assertEqual(cms_response.text, "Hello from CMS")

######### KEYCLOAK SMOKE TEST #########
keycloak_url = "http://localhost/auth/realms/safe-zone"
keycloak_response = requests.request("GET", keycloak_url, headers={}, data={})

class TestKeycloakSmokeTest(unittest.TestCase):
  def test_response_status_code(self):
    self.assertEqual(keycloak_response.status_code, 200)

######### WEB SMOKE TEST #########
web_url = "http://localhost"
web_response = requests.request("GET", web_url, headers={}, data={})

class TestWebSmokeTest(unittest.TestCase):
  def test_response_status_code(self):
    self.assertEqual(web_response.status_code, 200)

if __name__ == '__main__':
  unittest.main()

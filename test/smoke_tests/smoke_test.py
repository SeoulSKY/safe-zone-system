"""
Script used to run smoke tests
"""
import requests
import json
import unittest

SMOKE_TEST_RUNNING = False

def get_oauth_token(realm, id, secret):
  OAUTH_URL = "http://localhost/auth/realms/"+realm+"/protocol/openid-connect/token"
  OAUTH_HEADERS = { 'Content-Type': 'application/x-www-form-urlencoded' }
  OAUTH_PAYLOAD = 'grant_type=client_credentials&client_id='+id+'&client_secret='+secret
  response = requests.request("POST", OAUTH_URL, headers=OAUTH_HEADERS, data=OAUTH_PAYLOAD)
  access_token = json.loads(response.text)["access_token"]
  token_type = json.loads(response.text)["token_type"]
  return token_type + " " + access_token

######## MIBS SMOKE TEST #########
class TestMIBsSmokeTest(unittest.TestCase):
  def test_mibs_response_text(self):
    mibs_url = "http://localhost/mibs/hello"
    mibs_headers = {"Authorization": get_oauth_token("safe-zone", "safe-zone-client-credentials", "208d1d6c-fed9-4fe3-880b-62d667917ede")}
    mibs_response = requests.request("GET", mibs_url, headers=mibs_headers, data={})
    self.assertEqual(mibs_response.text, "Hello from MIBS")

######### CMS SMOKE TEST #########
class TestCMSSmokeTest(unittest.TestCase):
  def test_cms_response_text(self):
    cms_url = "http://localhost/cms/hello"
    cms_response = requests.request("GET", cms_url, headers={}, data={})
    self.assertEqual(cms_response.text, "Hello from CMS")

######### KEYCLOAK SMOKE TEST #########
class TestKeycloakSmokeTest(unittest.TestCase):
  def test_keycloak_response_status_code(self):
    keycloak_url = "http://localhost/auth/realms/safe-zone"
    keycloak_response = requests.request("GET", keycloak_url, headers={}, data={})
    self.assertEqual(keycloak_response.status_code, 200)

######### WEB SMOKE TEST #########
class TestWebSmokeTest(unittest.TestCase):
  def test_web_response_status_code(self):
    web_url = "http://localhost"
    web_response = requests.request("GET", web_url, headers={}, data={})
    self.assertEqual(web_response.status_code, 200)

######### ACCOUNT CREATION TEST #########
# class TestAccountCreation(unittest.TestCase):
#   def test_account_exists(self):
#     url = "http://localhost/auth/admin/realms/safe-zone/users"
#     token = get_oauth_token("master","admin-cli", " ")
#     print(token)
#     headers = {
#       'Content-Type': 'application/json',
#       'Authorization': token
#     }
#     payload = {
#       "enabled": "true", 
#       "firstName": "Test",
#       "lastName": "User",
#       "email": "test@test.com",
#       "username": "testaccount"
#     }
#     response = requests.request("POST", url, headers=headers, data=payload)
#     print(response.text)
#     self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
  unittest.main()

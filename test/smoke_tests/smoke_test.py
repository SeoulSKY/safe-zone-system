"""
Script used to run smoke tests
"""
import requests
import unittest

from keycloak import KeycloakOpenID

SMOKE_TEST_RUNNING = False


URL = 'http://localhost/auth/'
realm_name = 'safe-zone'

# Configure client
keycloak_openid = KeycloakOpenID(server_url=URL, client_id=realm_name, realm_name=realm_name)


def get_oauth_token():
    json = keycloak_openid.token("tester", "cmpt371")
    return json["token_type"] + " " + json["access_token"]


class TestMIBsSmokeTest(unittest.TestCase):
    """
    MIBS SMOKE TEST
    """

    def test_mibs_response_text(self):
        mibs_url = "http://localhost/mibs/hello"
        mibs_headers = {"Authorization": get_oauth_token()}
        mibs_response = requests.request("GET", mibs_url, headers=mibs_headers, data={})
        self.assertEqual(mibs_response.text, "Hello from MIBS")

    def test_mibs_unauthorized_access(self):
        mibs_url = "http://localhost/mibs/hello"
        mibs_response = requests.request("GET", mibs_url, data={})
        self.assertEqual(mibs_response.status_code, 401)


class TestKeycloakSmokeTest(unittest.TestCase):
    """
    KEYCLOAK SMOKE TEST
    """

    def test_keycloak_response_status_code(self):
        keycloak_url = "http://localhost/auth/realms/safe-zone"
        keycloak_response = requests.request("GET", keycloak_url, headers={}, data={})
        self.assertEqual(keycloak_response.status_code, 200)

# ######### ACCOUNT CREATION TEST #########
# class TestAccountCreation(unittest.TestCase):
#     def test_account_exists(self):
#      url = "http://localhost/auth/admin/realms/safe-zone/users"
#      token = get_oauth_token("master", "admin-cli", " ")
#      print(token)
#      headers = {
#        'Content-Type': 'application/json',
#        'Authorization': token
#      }
#      payload = {
#        "enabled": "true",
#        "firstName": "Test",
#        "lastName": "User",
#        "email": "test@test.com",
#        "username": "testaccount"
#      }
#      response = requests.request("POST", url, headers=headers, data=payload)
#      print(response.text)
#      self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()

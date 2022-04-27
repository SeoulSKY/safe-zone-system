import unittest, time, jwt
from unittest.mock import MagicMock
from flask import Flask
from auth import Authenticator, auth_token
from http import HTTPStatus
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


# Generate an RSA256 public/private key pair in order to self-sign tokens
# for testing.
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
private_pem = private_key.private_bytes(
    serialization.Encoding.PEM,
    serialization.PrivateFormat.TraditionalOpenSSL,
    serialization.NoEncryption()
).decode()
public_pem = private_key.public_key().public_bytes(
    serialization.Encoding.PEM,
    serialization.PublicFormat.PKCS1
).decode()


class TestAuthenticatorInit(unittest.TestCase):
    '''
    The test cases for the initialization of the `Authenticator`. This is a
    separate test case so that the authenticator can be initialized prior to 
    each test in `TestAuthenticator`.
    '''
    def test_init_no_app(self):
        '''
        Test that Authenticator can be initialized with no app given.
        '''
        auth = Authenticator()
        self.assertIsNone(auth.issuer)
        self.assertIsNone(auth.audience)
        self.assertIsNone(auth.jwks_client)
        self.assertEqual(auth._app_initialized, False)


    def test_no_issuer_provided(self):
        '''
        Test the assertion that there must be `ISSUER` in the app config.
        '''
        app = Flask(__name__)
        app.config.update({
            'TESTING': True,
            'AUTH_AUDIENCE': 'test',
            'AUTH_JWKS_URI': 'http://localhost/test/jwks',
        })
        with self.assertRaises(AssertionError):
            Authenticator(app)


    def test_no_audience_provided(self):
        '''
        Test the assertion that there must be `AUDIENCE` in the app config.
        '''
        app = Flask(__name__)
        app.config.update({
            'TESTING': True,
            'AUTH_ISSUER': 'test_issuer',
            'AUTH_JWKS_URI': 'http://localhost/test/jwks',
        })
        with self.assertRaises(AssertionError):
            Authenticator(app)


    def test_no_jwks_uri_provided(self):
        '''
        Test the assertion that there must be `JWKS_URI` in the app config.
        '''
        app = Flask(__name__)
        app.config.update({
            'TESTING': True,
            'AUTH_ISSUER': 'test_issuer',
            'AUTH_AUDIENCE': 'test',
        })
        with self.assertRaises(AssertionError):
            Authenticator(app)

    def test_attributes_data_type(self):
        '''
        test assertion for wrong data type
        '''
        app = Flask(__name__)
        app.config.update({
            'TESTING': True,
            'AUTH_ISSUER': 0,
            'AUTH_AUDIENCE': 0,
            'AUTH_JWKS_URI': 0,
        })
        with self.assertRaises(AssertionError):
            Authenticator(app)

    def test_init_valid(self):
        '''
        Test that Authenticator will initialize properly when given a valid
        app and app config.
        '''
        app = Flask(__name__)
        app.config.update({
            'TESTING': True,
            'AUTH_ISSUER': 'test_provider',
            'AUTH_AUDIENCE': 'test',
            'AUTH_JWKS_URI': 'http://localhost/test/jwks',
        })
        auth = Authenticator(app)
        self.assertEqual(auth.issuer, 'test_provider')
        self.assertEqual(auth.audience, 'test')
        self.assertEqual(auth.jwks_client.uri, 'http://localhost/test/jwks')
        self.assertEqual(auth._app_initialized, True)

    def test_init_invalid(self):
        '''
        Test that Authenticator will not initialize when given an invalid app
        '''
        app = "random"
        with self.assertRaises(AssertionError):
            Authenticator(app)


    def test_init_valid_later(self):
        '''
        Test that Authenticator initialized with no app can be provided an app
        later on.
        '''
        auth = Authenticator()
        app = Flask(__name__)
        app.config.update({
            'TESTING': True,
            'AUTH_ISSUER': 'test_provider',
            'AUTH_AUDIENCE': 'test',
            'AUTH_JWKS_URI': 'http://localhost/test/jwks',
        })
        auth.init_app(app)
        self.assertEqual(auth.issuer, 'test_provider')
        self.assertEqual(auth.audience, 'test')
        self.assertEqual(auth.jwks_client.uri, 'http://localhost/test/jwks')

    def test_init_invalid_later(self):
        '''
        Test that Authenticator initialized with no app, provided an invalid app
        later on will raise error
        '''
        auth = Authenticator()
        with self.assertRaises(AssertionError):
            auth.init_app("random")
        self.assertEqual(auth._app_initialized, False)


class TestAuthenticator(unittest.TestCase):
    '''
    The Test cases for the authenticator.
    '''
    def setUp(self) -> None:
        self.app = Flask(__name__)
        self.app.config.update({
            'TESTING': True,
            'AUTH_ISSUER': 'test_issuer',
            'AUTH_AUDIENCE': 'test',
            'AUTH_JWKS_URI': 'http://localhost/auth/jwks',
        })
        self.auth = Authenticator(self.app)

        mock_signing_key = MagicMock()
        mock_signing_key.key = public_pem

        mock_jwk_client = MagicMock()
        mock_jwk_client.get_signing_key_from_jwt = MagicMock(
            return_value=mock_signing_key
        )
        self.auth.jwks_client = mock_jwk_client
        

        @self.app.route('/test/protected', methods=['GET'])
        @self.auth.require_token
        def protected():
            return str(auth_token), HTTPStatus.OK
            

        @self.app.route('/test/unprotected', methods=['GET'])
        def unprotected():
            return str(auth_token), HTTPStatus.OK


    def test_jwks_provider_bad_connection(self):
        '''
        Test that errors connecting to the Auth Provider's JWKS are handled
        properly, and return a 500 Internal Server Error HTTP response.
        '''
        headers = {'alg': 'RS256', 'typ': 'JWT', 'kid': '0'}
        payload = {
            'iss': 'test_issuer',
            'exp': int(time.time()) + 30,
            'aud': 'test',
            'sub': 'test-user',
        }
        access_token = jwt.encode(payload, private_pem, 
            algorithm='RS256', 
            headers=headers
        )
        self.auth.jwks_client = jwt.PyJWKClient('http://localhost/auth/jwks')
        with self.app.test_client() as client:
            response = client.get('/test/protected', headers={
                'Authorization': 'Bearer ' + access_token
            })
            self.assertEqual(
                response.status_code, 
                HTTPStatus.INTERNAL_SERVER_ERROR
            )
            self.assertIsNotNone(response.get_json())

    def test_jwks_provider_json_response(self):
        '''
        Test that the json response being raised contains the correct information
        '''
        headers = {'alg': 'RS256', 'typ': 'JWT', 'kid': '0'}
        payload = {
            'iss': 'test_issuer',
            'exp': int(time.time()) + 30,
            'aud': 'test',
            'sub': 'test-user',
        }
        access_token = jwt.encode(payload, private_pem,
            algorithm='RS256',
            headers=headers
        )
        self.auth.jwks_client = jwt.PyJWKClient('http://localhost/auth/jwks')
        with self.app.test_client() as client:
            response = client.get('/test/protected', headers={
                'Authorization': 'Bearer ' + access_token
            })
            self.assertEqual(response.get_json()['error'], 'connection_error')
            self.assertEqual(response.get_json()['error_description'], 'cannot connect to auth provider')


    def test_require_auth_no_auth_header(self):
        '''
        Test that the require_auth decorator method handles requests with no
        Authorization header properly.
        '''
        with self.app.test_client() as client:
            response = client.get('/test/protected')
            self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
            self.assertIsNone(response.get_json())


    def test_require_auth_empty_header(self):
        '''
        Test that the require_auth decorator method handles requests with empty
        Authorization header.
        '''
        with self.app.test_client() as client:
            response = client.get('/test/protected', headers={})
            self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
            self.assertIsNone(response.get_json())


    def test_require_auth_invalid_auth_header(self):
        '''
        Test that the require_auth decorator method handles invalid 
        Authorization headers properly.
        '''
        with self.app.test_client() as client:
            response = client.get('/test/protected', headers={
                'Authorization': 'Code asdfghjkl'
             })
            self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
            self.assertIsNone(response.get_json())


    def test_require_auth_empty_auth_header(self):
        '''
        Test that the require_auth decorator method handles empty
        Authorization headers properly.
        '''
        with self.app.test_client() as client:
            response = client.get('/test/protected', headers={
                'Authorization': ''
             })
            self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
            self.assertIsNone(response.get_json())


    def test_require_auth_None_auth_header(self):
        '''
        Test that the require_auth decorator method handles empty
        Authorization headers properly.
        '''
        with self.app.test_client() as client:
            response = client.get('/test/protected', headers={
                'Authorization': None
             })
            self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
            self.assertIsNone(response.get_json())


    def test_require_auth_invalid_token_expired(self):
        '''
        Test that the require_auth decorator method handles requests sent with
        an access token that has expired.
        '''
        headers = {'alg': 'RS256', 'typ': 'JWT', 'kid': '0'}
        payload = {
            'iss': 'test_issuer',
            'exp': int(time.time()) - 30,
            'aud': 'test',
            'sub': 'test-user',
        }
        access_token = jwt.encode(payload, private_pem, 
            algorithm='RS256', 
            headers=headers
        )
        with self.app.test_client() as client:
            response = client.get('/test/protected', headers={
                'Authorization': 'Bearer ' + access_token
            })
            self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
            self.assertIsNotNone(response.get_json())


    def test_require_auth_invalid_token_expired_json_response(self):
        '''
        Test that the require_auth decorator method json response is correct.
        '''
        headers = {'alg': 'RS256', 'typ': 'JWT', 'kid': '0'}
        payload = {
            'iss': 'test_issuer',
            'exp': int(time.time()) - 30,
            'aud': 'test',
            'sub': 'test-user',
        }
        access_token = jwt.encode(payload, private_pem,
            algorithm='RS256',
            headers=headers
        )
        with self.app.test_client() as client:
            response = client.get('/test/protected', headers={
                'Authorization': 'Bearer ' + access_token
            })
            self.assertEqual(response.get_json()['error'], "invalid_token")
            self.assertEqual(response.get_json()['error_description'], "Signature has expired")


    def test_require_auth_invalid_claim(self):
        '''
        Test that the require_auth decorator method handles requests that 
        contains an access token with an invalid claim.
        '''
        headers = {'alg': 'RS256', 'typ': 'JWT', 'kid': '0'}
        payload = {
            'iss': 'test_issuer',
            'exp': int(time.time()) + 30,
            'aud': 'invalid-aud',
            'sub': 'test-user',
        }
        access_token = jwt.encode(payload, private_pem, 
            algorithm='RS256', 
            headers=headers
        )
        with self.app.test_client() as client:
            response = client.get('/test/protected', headers={
                'Authorization': 'Bearer ' + access_token
            })
            self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
            self.assertIsNotNone(response.get_json())

    def test_require_auth_invalid_claim_json(self):
        '''
        Test that the require_auth decorator method handles requests that
        contains an access token with an invalid claim.
        '''
        headers = {'alg': 'RS256', 'typ': 'JWT', 'kid': '0'}
        payload = {
            'iss': 'test_issuer',
            'exp': int(time.time()) + 30,
            'aud': 'invalid-aud',
            'sub': 'test-user',
        }
        access_token = jwt.encode(payload, private_pem,
            algorithm='RS256',
            headers=headers
        )
        with self.app.test_client() as client:
            response = client.get('/test/protected', headers={
                'Authorization': 'Bearer ' + access_token
            })
            self.assertEqual(response.get_json()['error'], 'invalid_token')
            self.assertEqual(response.get_json()['error_description'], 'Invalid audience')


    def test_require_auth_token_from_other_provider(self):
        '''
        Test that the require_auth decorator method handles requests sent with 
        an access token signed by an "outside" auth provider. Here, "Outside" 
        means it does not originate from the `AUTH_ISSUER` specified in the app
        config.
        '''
        # This token is the default rsa256 token from jwt.io
        access_token = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMj'
            'M0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTU'
            'xNjIzOTAyMn0.NHVaYe26MbtOYhSKkoKYdFVomg4i8ZJd8_-RU8VNbftc4TSMb4bX'
            'P3l3YlNWACwyXPGffz5aXHc6lty1Y2t4SWRqGteragsVdZufDn5BlnJl9pdR_kdVF'
            'Usra2rWKEofkZeIC4yWytE58sMIihvo9H1ScmmVwBcQP6XETqYd0aSHp1gOa9RdUP'
            'DvoXQ5oqygTqVtxaDr6wUFKrKItgBMzWIdNZ6y7O9E0DhEPTbE9rfBo6KTFsHAZnM'
            'g4k68CDp2woYIaXbmYTWcvbzIuHO7_37GT79XdIwkm95QJ7hYC9RiwrV7mesbY4PA'
            'ahERJawntho0my942XheVLmGwLMBkQ')
        with self.app.test_client() as client:
            response = client.get('/test/protected', headers={
                'Authorization': 'Bearer ' + access_token
            })
            self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
            self.assertIsNotNone(response.get_json())


    def test_require_auth_valid_token(self):
        '''
        Test that the require_auth decorator method allows the decorated route
        to be accessed.
        '''
        headers = {'alg': 'RS256', 'typ': 'JWT', 'kid': '0'}
        payload = {
            'iss': 'test_issuer',
            'exp': int(time.time()) + 30,
            'aud': 'test',
            'sub': 'test-user',
        }
        access_token = jwt.encode(payload, private_pem, 
            algorithm='RS256', 
            headers=headers
        )
        with self.app.test_client() as client:
            response = client.get('/test/protected', headers={
                'Authorization': 'Bearer ' + access_token
            })
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertEqual(response.data, str(payload).encode())


    def test_auth_token_unprotected(self):
        '''
        Test that the `auth_token` variable cannot be accessed from unprotected
        routes. i.e. if `auth_token` is set by one request to a protected 
        route, it should not be able to be accessed by a different, unprotected
        route.
        '''
        with self.app.test_client() as client:
            response = client.get('/test/unprotected')
            self.assertEqual(response.data, str(None).encode())


if __name__ == '__main__':
    unittest.main()

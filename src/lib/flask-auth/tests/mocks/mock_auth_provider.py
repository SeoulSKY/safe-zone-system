from urllib.error import URLError
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from jwt.exceptions import PyJWKClientError


class MockSigningKey(object):
    '''
    This class is a mock of the Signing key object that is returned by 
    `PyJWTClient.get_signing_key_from_jwt`.
    '''
    def __init__(self, key: bytes) -> None:
        self.key = key


class MockJWKClient(object):
    '''
    This class is a mock of PyJWKClient from PyJWT. It provides a way to check
    a JWT against a local JWKS rather that one at some URL.

    Attributes:
        jwks: a mock JSON Web Key Set that is used to validate given JWKs.
    '''
    def __init__(self, key: RSAPublicKey, conn: bool = True) -> None:
        '''
        Creates a Mock JWKClient. 

        Args:
            conn: whether or not a client connection can be established.
            key: the key to .
        '''
        self.connected = conn
        if key:
            self.key = key
        else:
            self.key = None


    def get_signing_key_from_jwt(self, token: str):
        '''
        Simulates a call to `PyJWTClient.get_signing_key_from_jwt` that is used
        by the `Authenticator` class.

        Args:
            token: the given JWT access token

        Returns:
            The mock client's key as a MockSigningKey

        Post-conditions:
            Raises URLError if self.connection == False 
            Raises PyJWKClientError if self.valid == False
        '''
        if not self.connected:
            raise URLError()
        
        if not self.key or not token:
            raise PyJWKClientError()

        return MockSigningKey(self.key)
from functools import wraps
from typing import Union
from flask import Flask, request, jsonify, _request_ctx_stack
from requests import Request
from auth.exceptions import AuthError
from jwt import decode, PyJWKClient
from jwt.exceptions import PyJWTError


class Authenticator(object):
  '''
  An authenticator for Oauth 2.0 access tokens.

  Attributes:
    issuer: The URL of the openid connect issuer
    audience: The audience of the service
    jwks_uri: The URI of the issuer's JWKS
  '''
  issuer: Union[str, None] = None
  audience: Union[str, None] = None
  jwks_uri: Union[str, None] = None

  def __init__(self, app: Flask):
    '''
    Initialize an access token authenticator for the given flask application.

    Args:
      app: The flask app

    Pre-conditions:
      AUTH_ISSUER in app.config
      AUTH_AUDIENCE in app.config
      AUTH_JWKS_URI in app.config
    '''
    config_keys = app.config.keys()
    assert('AUTH_ISSUER' in config_keys)
    assert('AUTH_AUDIENCE' in config_keys)
    assert('AUTH_JWKS_URI' in config_keys)

    self.issuer = app.config.get('AUTH_ISSUER')
    self.audience = app.config.get('AUTH_AUDIENCE')
    self.jwks_uri = app.config.get('AUTH_JWKS_URI')

    @app.errorhandler(AuthError)
    def handle_auth_error(error: AuthError):
      '''
      Returns a response based on an AuthError that has been raised. This
      function is called whenever an AuthError is raised inside of the flask
      app.
      '''
      response = jsonify(error.response)
      response.status_code = error.status_code
      return response

    @app.errorhandler(PyJWTError)
    def handle_pyjwt_error(error: PyJWTError):
      '''
      Returns a response based on an PyJWTError that has been raised. This
      function is called whenever an PyJWTError is raised inside of the flask
      app.
      '''
      response = jsonify({'error': str(error)})
      response.status_code = 401
      return response


  def require_auth(self, func):
    '''
    Requires that requests to the given route provide authentication via an
    access token passed in the Authentication header.

    This decorator should be called after @app.route(), so that it can inherit
    the request.

    Pre-conditions:
      this method is called after @Flask.route()

    Example:
      @app.route('/hello', methods=['POST','GET'])
      @auth.require_auth()
      def hello():
        return 'Hello World!'
    '''
    @wraps(func)
    def wrapped_route(*args, **kwargs):
      '''
      The route function that wrapped by require_auth
      '''
      token = get_access_token(request)
      jwks_client = PyJWKClient(self.jwks_uri)
      signing_key = jwks_client.get_signing_key_from_jwt(token)

      data = decode(token, 
        signing_key.key, 
        algorithms=["RS256"],
        issuer=self.issuer,
        audience=self.audience,
      )
      return func(*args, **kwargs)
    return wrapped_route


def get_access_token(request: Request) -> str:
  '''
  Retrieves the access token from the Authorization Header of a given
  request.

  Post-conditions:
    Raises an AuthError if the request does not have an Authorization header.
  '''
  auth = request.headers.get('Authorization', None)
  if (auth == None):
      raise AuthError(401)

  return parse_token_from_header(auth)


def parse_token_from_header(authorization: str) -> str:
  '''
  Parses an access token from a given Authorization header value. Note that 
  this function does not verify the token.

  Pre-conditions:
    authorization != None

  Post-conditions:
    Raises AuthError if the token cannot be parsed. Due to 
  '''
  assert(authorization != None)

  parts = authorization.split()
  if len(parts) != 2 or parts[0] != 'Bearer':
    raise AuthError(401)
  
  return parts[1]

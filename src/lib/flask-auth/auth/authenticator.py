from functools import wraps
from typing import Union
from flask import Flask, request, jsonify, _request_ctx_stack
from jwt import decode, PyJWKClient
from jwt.exceptions import PyJWTError, InvalidTokenError
from auth.exceptions import *
from auth.utils import get_access_token
from werkzeug.local import LocalProxy


# allows flask applications to access the auth token
auth_token = LocalProxy(lambda: 
  getattr(_request_ctx_stack.top, 'auth_token', None)
)


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
    Creates an access token authenticator for the given flask application.

    Args:
      app: The flask app

    Pre-conditions:
      AUTH_ISSUER in app.config
      AUTH_AUDIENCE in app.config
      AUTH_JWKS_URI in app.config

    Post-conditions:
      Registers error handler with app that catches authentication errors and
      returns the an appropriate response.
    '''
    config_keys = app.config.keys()
    assert 'AUTH_ISSUER' in config_keys
    assert 'AUTH_AUDIENCE' in config_keys
    assert 'AUTH_JWKS_URI' in config_keys

    self.issuer = app.config.get('AUTH_ISSUER')
    self.audience = app.config.get('AUTH_AUDIENCE')
    self.jwks_client = PyJWKClient(app.config.get('AUTH_JWKS_URI'))
    
    @app.errorhandler(PyJWTError)
    def handle_pyjwt_error(error: PyJWTError):
      '''
      Returns a response based on a PyJWTError that has been raised. This
      function is called when PyJWTErrors are raised inside of app.
      '''
      if (isinstance(error, InvalidTokenError)):
        response = jsonify({
          'error': 'invalid_token',
          'error_description': str(error)
        })
        response.status_code = 401
        return response
      else:
        response = jsonify(None)
        response.status_code = 401
        return response


  def require_token(self, func):
    '''
    Decorator that requires that requests to the decorated route provide
    authentication via an access token passed in the Authentication header.

    Args:
      func: the function that require_token decorates

    Example:
      @app.route('/hello', methods=['POST','GET'])
      @auth.require_auth
      def hello():
        return 'Hello World!'
    '''
    @wraps(func)
    def wrapped_route(*args, **kwargs):
      '''
      The route function that wrapped by require_auth
      '''
      token = get_access_token(request)
      signing_key = self.jwks_client.get_signing_key_from_jwt(token)

      data = decode(token, 
        signing_key.key, 
        algorithms=["RS256"],
        issuer=self.issuer,
        audience=self.audience,
      )
      _request_ctx_stack.top.auth_token = data
      return func(*args, **kwargs)
    return wrapped_route
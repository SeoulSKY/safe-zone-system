'''
The errors that may occur during the authentication process.
'''
from http import HTTPStatus


class AuthError(Exception):
  '''
  The base authentication error. AuthError is a sub class of PyJWTError because
  it allows for a single flask error handler to be used for all errors in the
  authentication process.
  '''
  error: str = None
  status_code: int = HTTPStatus.UNAUTHORIZED

  def __init__(self, message: str = None) -> None:
    '''
    Initialize an authentication error.
    '''
    self.error_description = message
    super().__init__(message)


class InvalidTokenError(AuthError):
  '''
  An authorization error due to an invalid access token provided in the request
  Authorization header.
  '''
  def __init__(self, message) -> None:
    '''
    Initialize an invalid token error.
    '''
    super().__init__(message)
    self.error = 'invalid_token'


class MissingAuthError(AuthError):
  '''
  An authorization error due to a missing Authorization header in the request.
  '''
  pass

class MalformedAuthError(AuthError):
  '''
  An authorization error due to a malformed Authorization header in the request.
  '''
  pass

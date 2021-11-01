'''
The errors that may occur during the authentication process.
'''
from jwt.exceptions import PyJWTError


class AuthError(PyJWTError):
  '''
  The base authentication error. AuthError is a sub class of PyJWTError because
  it allows for a single flask error handler to be used for all errors in the
  authentication process.
  '''
  pass

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

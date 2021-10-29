'''
Utility functions for the authentication library.
'''
from requests import Request
from auth.exceptions import *


def get_access_token(request: Request) -> str:
  '''
  Retrieves the access token from the Authorization Header of a given
  request.

  Post-conditions:
    Raises an MissingAuthError if the request does not have an 
    Authorization header.
  '''
  auth = request.headers.get('Authorization', None)
  if (auth == None):
      raise MissingAuthError()

  return parse_token_from_auth(auth)


def parse_token_from_auth(authorization: str) -> str:
  '''
  Parses an access token from a given Authorization header value. Note that 
  this function does not verify the token.

  Pre-conditions:
    authorization != None

  Post-conditions:
    Raises MalformedAuthError if the token cannot be parsed.
  '''
  assert authorization != None

  parts = authorization.split()
  if len(parts) != 2 or parts[0] != 'Bearer':
    raise MalformedAuthError()
  
  return parts[1]
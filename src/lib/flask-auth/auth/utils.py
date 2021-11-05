'''
Utility functions for the authentication library.
'''
from requests import Request
from auth.exceptions import *


def get_access_token(request: Request) -> str:
    '''
    Retrieves the access token from the Authorization Header of a given
    request.

    Pre-conditions:
        request != None

    Post-conditions:
        Raises an MissingAuthError if the request does not have an 
        Authorization header.
        Raises MalformedAuthError if the token cannot be parsed.
    '''
    assert request != None

    auth = request.headers.get('Authorization', None)
    if (auth == None):
        raise MissingAuthError()

    return __parse_token_from_auth(auth)


def __parse_token_from_auth(authorization: str) -> str:
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
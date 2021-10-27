'''
The errors that may occur during the authentication process.
'''

from typing import Union


class AuthError(Exception):
  '''
  Represents an error with the authentication of a request.

  Attributes:
    response: A dict containing the error response.
    status_code: the HTTP status code of the error respose.
  '''
  def __init__(self, 
    status_code: int, 
    response: Union[dict, None] = None
  ) -> None:
    '''
    An error with the authentication of a request.

    Args:
      error: the error response.
      status_code: the HTTP status code of the error respose.
    '''
    self.response = response
    self.status_code = status_code

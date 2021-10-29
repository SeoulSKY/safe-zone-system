import unittest, sys
from requests import Request

sys.path.append('../')

from auth.utils import *
from auth.exceptions import *


class TestUtils(unittest.TestCase):
  '''
  The test cases for all the utility functions.
  '''

  def test_parse_token_from_auth(self):
    '''
    Test the parse_token_from_auth() function.
    '''
    # case: valid authorization header string
    self.assertEqual(parse_token_from_auth('Bearer asdf'), 'asdf')

    # case: empty string
    with self.assertRaises(MalformedAuthError):
      parse_token_from_auth('')

    # case: invalid header prefix
    with self.assertRaises(MalformedAuthError):
      parse_token_from_auth('Token asdf')

    # case: violate !None precondition
    with self.assertRaises(AssertionError):
      parse_token_from_auth(None),


  def test_get_access_token(self):
    '''
    Test the get_access_token() function
    '''
    # case: auth header, valid value
    self.assertEqual(
      get_access_token(Request(headers={'Authorization': 'Bearer asdf'})),
      'asdf'
    )
    # case: no Auth header
    with self.assertRaises(MissingAuthError):
      get_access_token(Request())

    # case: auth header exits, None value
    with self.assertRaises(MissingAuthError):
      get_access_token(Request(headers={'Authorization': None}))

    # case: auth header exists, invalid header prefix
    with self.assertRaises(MalformedAuthError):
      get_access_token(Request(headers={'Authorization': 'Token asdf'}))


if __name__ == '__main__':
    unittest.main()
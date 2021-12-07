import unittest
from requests import Request
from auth.utils import get_access_token
from auth.exceptions import *


class TestGetAccessToken(unittest.TestCase):
    '''
    The test cases for the get_access_token function.
    '''
    def test_valid_request(self):
        '''
        Test Case:
        Request has an Authorization header with a valid value.
        '''
        self.assertEqual(
            get_access_token(Request(
                headers={'Authorization': 'Bearer asdf'}
            )),
            'asdf'
        )


    def test_no_auth_header_value(self):
        '''
        Test Case:
        Request has an Authorization header with a value of None.
        '''
        with self.assertRaises(MissingAuthError):
            get_access_token(Request(headers={'Authorization': None}))

    def test_no_auth_empty_header_value(self):
        '''
        Test Case:
        Request has an Authorization header with an empty string
        '''
        with self.assertRaises(MissingAuthError):
            get_access_token(Request(headers={'Authorization': ""}))

    def test_no_auth_empty_header(self):
        '''
        Test Case:
        Request has an Authorization header with an empty dictionary
        '''
        with self.assertRaises(MissingAuthError):
            get_access_token(Request(headers={}))


    def test_no_auth_header(self):
        '''
        Test Case:
        Request has no Authorization header.
        '''
        with self.assertRaises(MissingAuthError):
            get_access_token(Request())


    def test_no_auth_header_wrong_string(self):
        '''
        Test Case:
        Request has wrong string in header
        '''
        with self.assertRaises(MissingAuthError):
            get_access_token(Request(headers={"random": "random"}))


    def test_invalid_header_prefix(self):
        '''
        Test Case:
        Request has an Authorization header with a value that contains an
        invalid header prefix.
        '''
        with self.assertRaises(MalformedAuthError):
            get_access_token(Request(headers={'Authorization': 'Token asdf'}))


    def test_no_request_wrong_type(self):
        '''
        Test Case:
        Request is of wrong data type
        '''
        with self.assertRaises(AssertionError):
            get_access_token("Request"),

    def test_no_request(self):
        '''
        Test Case:
        Request is None.
        '''
        with self.assertRaises(AssertionError):
            get_access_token(None),



if __name__ == '__main__':
    unittest.main()
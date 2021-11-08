import unittest, sys
from requests import Request
from auth.utils import get_access_token
from auth.exceptions import *


class TestGetAccessToken(unittest.TestCase):
	'''
	The test cases for the get_access_token function.
	'''
	def valid_request(self):
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
   

	def no_auth_header_value(self):
		'''
		Test Case: 
		Request has an Authorization header with a value of None.
		'''
		with self.assertRaises(MissingAuthError):
			get_access_token(Request(headers={'Authorization': None}))


	def no_auth_header(self):
		'''
		Test Case: 
		Request has no Authorization header.
		'''
		with self.assertRaises(MissingAuthError):
			get_access_token(Request())


	def invalid_header_prefix(self):
		'''
		Test Case: 
		Request has an Authorization header with a value that contains an 
		invalid header prefix.
		'''
		with self.assertRaises(MalformedAuthError):
			get_access_token(Request(headers={'Authorization': 'Token asdf'}))


	def test_no_request(self):
		'''
		Test Case:
		Request is None.
		'''
		with self.assertRaises(AssertionError):
			get_access_token(None),



if __name__ == '__main__':
    unittest.main()
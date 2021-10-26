'''
/mibs endpoint unit tests
'''

import unittest

import re
from urllib.parse import urlparse, parse_qs
from dateutil.parser import parse as datetimeParse
from api.mibs import mibs_blueprint, TEMP_USER_ID
from models import Message, db
from flask import Flask
from http import HTTPStatus


class TestMibsApi(unittest.TestCase):
    '''
    /mibs endpoint unit tests
    '''
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
        self.app.register_blueprint(mibs_blueprint)

        self.client = self.app.test_client()

        self.test_message = {
            'message': 'test message',
            'recipients': [
            {
                'email': 'test@email.com'
            }
            ],
            'sendTime': '2021-10-27T23:22:19.911Z'
        }

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


    def test_post_not_json(self):
        '''
        Test POST /mibs when content type is not application/json
        '''
        response = self.client.post(
            '/mibs',
            content_type='application/x-www-form-urlencoded',
            json=self.test_message
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'Request is not JSON')

    def test_post_missing_message(self):
        '''
        Test POST /mibs when request body is missing field "message"
        '''
        self.test_message.pop('message')
        response = self.client.post(
            '/mibs',
            json=self.test_message
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'"message" missing from request body')

    def test_post_missing_recipients(self):
        '''
        Test POST /mibs when request body is missing field "recipients"
        '''
        self.test_message.pop('recipients')
        response = self.client.post(
            '/mibs',
            json=self.test_message
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'"recipients" missing from request body')

    def test_post_empty_recipients(self):
        '''
        Test POST /mibs when request body's recipients field is an empty array
        '''
        self.test_message['recipients'] = []
        response = self.client.post(
            '/mibs',
            json=self.test_message
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'Must have atleast 1 recipient')

    def test_post_invalid_recipients(self):
        '''
        Test POST /mibs when request body's recipients field container invalid recipients
        '''
        test_email = 'test@email.com'
        test_phone_number = 'testPhoneNumber'
        test_user_id = 'testUserId'
        test_invalid = 'testInvalid'
        self.test_message['recipients'] = [
            {'email': test_email},
            {'phoneNumber': test_phone_number},
            {'userId': test_user_id},
            {'invalid': test_invalid},
        ]
        response = self.client.post(
            '/mibs',
            json=self.test_message
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertNotIn(test_email.encode(), response.data)
        self.assertIn(test_phone_number.encode(), response.data)
        self.assertIn(test_user_id.encode(), response.data)
        self.assertIn(test_invalid.encode(), response.data)

    def test_post_missing_send_time(self):
        '''
        Test POST /mibs when request body is missing field "sendTime"
        '''
        self.test_message.pop('sendTime')
        response = self.client.post(
            '/mibs',
            json=self.test_message
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'"sendTime" missing from request body')

    def test_post_invalid_send_time(self):
        '''
        Test POST /mibs when request body's sendTime field is not an ISO-8601 datetime
        '''
        self.test_message['sendTime'] = '2021-10-27T23:22:19.911Za'
        response = self.client.post(
            '/mibs',
            json=self.test_message
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'"sendTime" is not an ISO-8601 UTC date time string')

    def test_post_success_1_recipient(self):
        '''
        Test POST /mibs when request is successful with one recipient
        '''
        response = self.client.post(
            '/mibs',
            json=self.test_message
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn('Location', response.headers)
        self.assertRegex(response.headers['Location'], re.compile(r'^.*/mibs\?messageId=\d+$'))
        self.assertEqual(response.data, b'MessageInABottle was successfully created')

        message_id = int(parse_qs(urlparse(response.headers['Location']).query)['messageId'][0])

        with self.app.app_context():
            message = Message.query.get(message_id)

            self.assertEqual(message.message_id, message_id)
            self.assertEqual(message.user_id, TEMP_USER_ID)
            self.assertEqual(message.message, self.test_message['message'])
            self.assertFalse(message.sent)
            self.assertIsNone(message.last_sent_time)
            self.assertEqual(message.send_time,
                datetimeParse(self.test_message['sendTime']).replace(tzinfo=None))

            self.assertFalse(message.sent)
            self.assertEqual(len(message.email_recipients), 1)
            self.assertEqual(message.email_recipients[0].email,
                self.test_message['recipients'][0]['email'])
            self.assertFalse(message.email_recipients[0].sent)
            self.assertIsNone(message.email_recipients[0].send_attempt_time)

    def test_post_success_many_recipients(self):
        '''
        Test POST /mibs when request is successful with more than one recipient
        '''
        self.test_message['recipients'] = [
            {'email': 'test1@email.com'},
            {'email': 'test2@email.com'}
        ]
        response = self.client.post(
            '/mibs',
            json=self.test_message
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        message_id = int(parse_qs(urlparse(response.headers['Location']).query)['messageId'][0])

        with self.app.app_context():
            message = Message.query.get(message_id)

            self.assertEqual(len(message.email_recipients), 2)
            self.assertEqual(message.email_recipients[0].email,
                self.test_message['recipients'][0]['email'])
            self.assertFalse(message.email_recipients[0].sent)
            self.assertEqual(message.email_recipients[1].email,
                self.test_message['recipients'][1]['email'])
            self.assertFalse(message.email_recipients[1].sent)

if __name__ == '__main__':
    unittest.main()

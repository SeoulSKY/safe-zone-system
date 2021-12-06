'''
/mibs endpoint unit tests
'''
import unittest

import time
import jwt
import re
from urllib.parse import urlparse, parse_qs
from dateutil.parser import parse as datetimeParse
from datetime import datetime
from api.mibs import mibs_blueprint, delete_mibs_for_user
from models import Message, EmailMessageRecipient, db
from flask import Flask
from http import HTTPStatus
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from auth_init import auth
from unittest.mock import MagicMock

test_email = 'test@email.com'
test_user_id = 'test-user'
test_other_user = 'other_user'
test_message_id = 1
test_message_id2 = 2

# Generate an RSA256 public/private key pair in order to self-sign tokens
# for testing.
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
private_pem = private_key.private_bytes(
    serialization.Encoding.PEM,
    serialization.PrivateFormat.TraditionalOpenSSL,
    serialization.NoEncryption()
).decode()
public_pem = private_key.public_key().public_bytes(
    serialization.Encoding.PEM,
    serialization.PublicFormat.PKCS1
).decode()


class TestMibsApi(unittest.TestCase):
    '''
    /mibs endpoint unit tests
    '''

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['AUTH_ISSUER'] = 'test_issuer'
        self.app.config['AUTH_AUDIENCE'] = 'test'
        self.app.config['AUTH_JWKS_URI'] = 'http://localhost/test/jwks'
        auth.init_app(self.app)
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            db.engine.execute('PRAGMA foreign_keys=ON')
        self.app.register_blueprint(mibs_blueprint)

        self.client = self.app.test_client()

        self.test_post_message = {
            'message': 'test message',
            'recipients': [
            {
                'email': 'test@email.com'
            }
            ],
            'sendTime': '2021-10-27T23:22:19.911Z'
        }

        self.test_put_message = {
            'messageId': 1,
            'message': 'new test message',
            'recipients': [
            {
                'email': 'new.test@email.com'
            }
            ],
            'sendTime': '2021-10-27T23:22:19.911Z'
        }
        mock_signing_key = MagicMock()
        mock_signing_key.key = public_pem

        mock_jwk_client = MagicMock()
        mock_jwk_client.get_signing_key_from_jwt = MagicMock(
            return_value=mock_signing_key
        )
        auth.jwks_client = mock_jwk_client


        self.test_post_invalid_email_recipient_1 = {
            'message': 'test message',
            'recipients': [
            {
                'email': 'test'
            }
            ],
            'sendTime': '2021-10-27T23:22:19.911Z'
        }

        self.test_post_invalid_email_recipient_2 = {
            'message': 'test message',
            'recipients': [
            {
                'email': 'test@'
            }
            ],
            'sendTime': '2021-10-27T23:22:19.911Z'
        }

        self.test_post_invalid_email_recipient_3 = {
            'message': 'test message',
            'recipients': [
            {
                'email': 'test@.com'
            }
            ],
            'sendTime': '2021-10-27T23:22:19.911Z'
        }

        self.test_put_invalid_email_recipient_1= {
            'messageId': 1,
            'message': 'new test message',
            'recipients': [
            {
                'email': 'test'
            }
            ],
            'sendTime': '2021-10-27T23:22:19.911Z'
        }

        self.test_put_invalid_email_recipient_2= {
            'messageId': 1,
            'message': 'new test message',
            'recipients': [
            {
                'email': 'test@'
            }
            ],
            'sendTime': '2021-10-27T23:22:19.911Z'
        }

        self.test_put_invalid_email_recipient_3= {
            'messageId': 1,
            'message': 'new test message',
            'recipients': [
            {
                'email': 'test@.com'
            }
            ],
            'sendTime': '2021-10-27T23:22:19.911Z'
        }

        self.test_put_invalid_message_id_recipient= {
            'messageId': 'helloUniverse',
            'message': 'new test message',
            'recipients': [
            {
                'email': 'test@.com'
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
            headers={'Authorization': 'Bearer ' + self.get_token()},
            json=self.test_post_message
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'Request is not JSON')

    def test_post_invalid_email_1(self):
        '''
        Test POST /mibs when request body is using an invalid email
        '''
        response = self.client.post(
            '/mibs',
            json=self.test_post_invalid_email_recipient_1,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'invalid email in request body')

    def test_post_invalid_email_2(self):
        '''
        Test POST /mibs when request body is using an invalid email
        '''
        response = self.client.post(
            '/mibs',
            json=self.test_post_invalid_email_recipient_2,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_post_invalid_email_3(self):
        '''
        Test POST /mibs when request body is using an invalid email
        '''
        response = self.client.post(
            '/mibs',
            json=self.test_post_invalid_email_recipient_3,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'invalid email in request body')

    def test_put_invalid_email_1(self):
        '''
        Test PUT /mibs when request body is using an invalid email
        '''
        response = self.client.put(
            '/mibs',
            json=self.test_put_invalid_email_recipient_1,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'invalid email in request body')

    def test_put_invalid_email_2(self):
        '''
        Test PUT /mibs when request body is using an invalid email
        '''
        response = self.client.put(
            '/mibs',
            json=self.test_put_invalid_email_recipient_2,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'invalid email in request body')

    def test_put_invalid_email_3(self):
        '''
        Test PUT /mibs when request body is using an invalid email:
        '''
        response = self.client.put(
            '/mibs',
            json=self.test_put_invalid_email_recipient_3,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'invalid email in request body')

    def test_put_invalid_message_id(self):
        '''
        Test PUT /mibs when request body is using an invalid message_id:
        '''
        response = self.client.put(
            '/mibs',
            json= self.test_put_invalid_message_id_recipient,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'invalid messageId: messageId must be an integer')

    def test_post_missing_message(self):
        '''
        Test POST /mibs when request body is missing field "message"
        '''
        self.test_post_message.pop('message')
        response = self.client.post(
            '/mibs',
            json=self.test_post_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'"message" missing from request body')

    def test_post_missing_recipients(self):
        '''
        Test POST /mibs when request body is missing field "recipients"
        '''
        self.test_post_message.pop('recipients')
        response = self.client.post(
            '/mibs',
            json=self.test_post_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'"recipients" missing from request body')

    def test_post_empty_recipients(self):
        '''
        Test POST /mibs when request body's recipients field is an empty array
        '''
        self.test_post_message['recipients'] = []
        response = self.client.post(
            '/mibs',
            json=self.test_post_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'Must have at least 1 recipient')

    def test_post_invalid_recipients(self):
        '''
        Test POST /mibs when request body's recipients field container invalid recipients
        '''
        test_phone_number = 'testPhoneNumber'
        test_invalid = 'testInvalid'
        self.test_post_message['recipients'] = [
            {'email': test_email},
            {'phoneNumber': test_phone_number},
            {'userId': test_user_id},
            {'invalid': test_invalid},
        ]
        response = self.client.post(
            '/mibs',
            json=self.test_post_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
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
        self.test_post_message.pop('sendTime')
        response = self.client.post(
            '/mibs',
            json=self.test_post_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'"sendTime" missing from request body')

    def test_post_invalid_send_time(self):
        '''
        Test POST /mibs when request body's sendTime field is not an ISO-8601 datetime
        '''
        self.test_post_message['sendTime'] = '2021-10-27T23:22:19.911Za'
        response = self.client.post(
            '/mibs',
            json=self.test_post_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'"sendTime" is not an ISO-8601 UTC date time string')

    def test_post_success_1_recipient(self):
        '''
        Test POST /mibs when request is successful with one recipient
        '''
        response = self.client.post(
            '/mibs',
            json=self.test_post_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIn('Location', response.headers)
        self.assertRegex(response.headers['Location'], re.compile(r'^.*/mibs\?messageId=\d+$'))
        self.assertEqual(response.data, b'MessageInABottle was successfully created')

        message_id = int(parse_qs(urlparse(response.headers['Location']).query)['messageId'][0])

        with self.app.app_context():
            message = Message.query.get(message_id)

            self.assertEqual(message.message_id, message_id)
            self.assertEqual(message.user_id, test_user_id)
            self.assertEqual(message.message, self.test_post_message['message'])
            self.assertFalse(message.sent)
            self.assertIsNone(message.last_sent_time)
            self.assertEqual(message.send_time,
                datetimeParse(self.test_post_message['sendTime']).replace(tzinfo=None))

            self.assertFalse(message.sent)
            self.assertEqual(len(message.email_recipients), 1)
            self.assertEqual(message.email_recipients[0].email,
                self.test_post_message['recipients'][0]['email'])
            self.assertFalse(message.email_recipients[0].sent)
            self.assertIsNone(message.email_recipients[0].send_attempt_time)

    def test_post_success_many_recipients(self):
        '''
        Test POST /mibs when request is successful with more than one recipient
        '''
        self.test_post_message['recipients'] = [
            {'email': 'test1@email.com'},
            {'email': 'test2@email.com'}
        ]
        response = self.client.post(
            '/mibs',
            json=self.test_post_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        message_id = int(parse_qs(urlparse(response.headers['Location']).query)['messageId'][0])

        with self.app.app_context():
            message = Message.query.get(message_id)

            self.assertEqual(len(message.email_recipients), 2)
            self.assertEqual(message.email_recipients[0].email,
                self.test_post_message['recipients'][0]['email'])
            self.assertFalse(message.email_recipients[0].sent)
            self.assertEqual(message.email_recipients[1].email,
                self.test_post_message['recipients'][1]['email'])
            self.assertFalse(message.email_recipients[1].sent)

    def test_put_not_json(self):
        '''
        Test PUT /mibs when content type is not application/json
        '''
        response = self.client.put(
            '/mibs',
            content_type='application/x-www-form-urlencoded',
            json=self.test_put_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'Request is not JSON')

    def test_put_missing_message_id(self):
        '''
        Test PUT /mibs when request body is missing field "message"
        '''
        self.test_put_message.pop('messageId')
        response = self.client.put(
            '/mibs',
            json=self.test_put_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'"messageId" missing from request body')

    def test_put_missing_message(self):
        '''
        Test PUT /mibs when request body is missing field "message"
        '''
        self.test_put_message.pop('message')
        response = self.client.put(
            '/mibs',
            json=self.test_put_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'"message" missing from request body')

    def test_put_missing_recipients(self):
        '''
        Test PUT /mibs when request body is missing field "recipients"
        '''
        self.test_put_message.pop('recipients')
        response = self.client.put(
            '/mibs',
            json=self.test_put_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'"recipients" missing from request body')

    def test_put_empty_recipients(self):
        '''
        Test PUT /mibs when request body's recipients field is an empty array
        '''
        self.test_put_message['recipients'] = []
        response = self.client.put(
            '/mibs',
            json=self.test_put_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'Must have at least 1 recipient')

    def test_put_invalid_recipients(self):
        '''
        Test PUT /mibs when request body's recipients field container invalid recipients
        '''
        test_phone_number = 'testPhoneNumber'
        test_invalid = 'testInvalid'
        self.test_put_message['recipients'] = [
            {'email': test_email},
            {'phoneNumber': test_phone_number},
            {'userId': test_user_id},
            {'invalid': test_invalid},
        ]
        response = self.client.put(
            '/mibs',
            json=self.test_put_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertNotIn(test_email.encode(), response.data)
        self.assertIn(test_phone_number.encode(), response.data)
        self.assertIn(test_user_id.encode(), response.data)
        self.assertIn(test_invalid.encode(), response.data)

    def test_put_missing_send_time(self):
        '''
        Test PUT /mibs when request body is missing field "sendTime"
        '''
        self.test_put_message.pop('sendTime')
        response = self.client.put(
            '/mibs',
            json=self.test_put_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'"sendTime" missing from request body')

    def test_put_invalid_send_time(self):
        '''
        Test PUT /mibs when request body's sendTime field is not an ISO-8601 datetime
        '''
        self.test_put_message['sendTime'] = '2021-10-27T23:22:19.911Za'
        response = self.client.put(
            '/mibs',
            json=self.test_put_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'"sendTime" is not an ISO-8601 UTC date time string')

    def test_put_no_message_in_database(self):
        '''
        Test PUT /mibs when the messageId does not exist in the database
        '''
        response = self.client.put(
            '/mibs',
            json=self.test_put_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'a message with messageId=1 could not be found')

    def test_put_message_already_sent(self):
        '''
        Test PUT /mibs when the sent column of the message is True
        '''

        with self.app.app_context():
            db.session.add(Message(
                message_id=self.test_put_message['messageId'],
                user_id=test_user_id,
                message=self.test_put_message['message'],
                send_time=datetime.now(),
                sent=True
            ))
            db.session.commit()

        response = self.client.put(
            '/mibs',
            json=self.test_put_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'message already sent')

    def test_put_message_already_partialy_sent(self):
        '''
        Test PUT /mibs when the lastSentTime of the message is set
        '''
        with self.app.app_context():
            db.session.add(Message(
                message_id=self.test_put_message['messageId'],
                user_id=test_user_id,
                message=self.test_put_message['message'],
                send_time=datetime.now(),
                last_sent_time=datetime.now()
            ))
            db.session.commit()

        response = self.client.put(
            '/mibs',
            json=self.test_put_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'message already sent')

    def test_put_success(self):
        '''
        Test PUT /mibs when request is successful
        '''

        self.create_message()

        response = self.client.put(
            '/mibs',
            json=self.test_put_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn('Location', response.headers)
        self.assertEqual(response.data, b'MessageInABottle was successfully updated')

        with self.app.app_context():
            message = Message.query.get(self.test_put_message['messageId'])

            self.assertEqual(message.message_id, self.test_put_message['messageId'])
            self.assertEqual(message.user_id, test_user_id)
            self.assertEqual(message.message, self.test_put_message['message'])
            self.assertFalse(message.sent)
            self.assertIsNone(message.last_sent_time)
            self.assertEqual(message.send_time,
                datetimeParse(self.test_put_message['sendTime']).replace(tzinfo=None))

            self.assertFalse(message.sent)
            self.assertEqual(len(message.email_recipients), 1)
            self.assertEqual(message.email_recipients[0].email,
                self.test_put_message['recipients'][0]['email'])
            self.assertFalse(message.email_recipients[0].sent)
            self.assertIsNone(message.email_recipients[0].send_attempt_time)

    def test_put_success_add_recipients(self):
        '''
        Test POST /mibs when request is successful when adding a recipient
        '''

        self.create_message()

        self.test_put_message['recipients'] = [
            {'email': 'test1@email.com'},
            {'email': 'test2@email.com'}
        ]
        response = self.client.put(
            '/mibs',
            json=self.test_put_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        with self.app.app_context():
            message = Message.query.get(self.test_put_message['messageId'])

            self.assertEqual(len(message.email_recipients), 2)
            self.assertEqual(message.email_recipients[0].email,
                self.test_put_message['recipients'][0]['email'])
            self.assertFalse(message.email_recipients[0].sent)
            self.assertEqual(message.email_recipients[1].email,
                self.test_put_message['recipients'][1]['email'])
            self.assertFalse(message.email_recipients[1].sent)

    def test_put_success_remove_recipients(self):
        '''
        Test POST /mibs when request is successful when removing a recipient
        '''

        self.create_message()
        self.create_email_recipient(
            message_send_request_id=1,
            email=self.test_put_message['recipients'][0]['email']
        )
        self.create_email_recipient(message_send_request_id=2)

        response = self.client.put(
            '/mibs',
            json=self.test_put_message,
            headers={'Authorization': 'Bearer ' + self.get_token()}
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        with self.app.app_context():
            message = Message.query.get(self.test_put_message['messageId'])

            self.assertEqual(len(message.email_recipients), 1)
            self.assertEqual(message.email_recipients[0].email,
                self.test_put_message['recipients'][0]['email'])
            self.assertFalse(message.email_recipients[0].sent)

    def test_delete_mibs_for_user_all_no_mibs(self):
        '''
        Test delete_mibs_for_user when its used to delete all mibs when the user has no mibs
        '''
        with self.app.app_context():
            self.assertFalse(delete_mibs_for_user(test_user_id, None))
            self.assertEqual(None, Message.query.get(test_message_id))

    def test_delete_mibs_for_user_all_no_mibs_but_another_user_has_a_mib(self):
        '''
        Test delete_mibs_for_user when its used to delete all mibs when the user has no mibs
        but another user has a mib
        '''
        self.create_message(user_id=test_other_user)
        with self.app.app_context():
            self.assertFalse(delete_mibs_for_user(test_user_id, None))
            self.assertNotEqual(None, Message.query.get(test_message_id))

    def test_delete_mibs_for_user_all_one_mib(self):
        '''
        Test delete_mibs_for_user when its used to delete all mibs when the user has one mib
        '''
        self.create_message()
        with self.app.app_context():
            self.assertTrue(delete_mibs_for_user(test_user_id, None))
            self.assertEqual(None, Message.query.get(test_message_id))

    def test_delete_mibs_for_user_all_two_mibs(self):
        '''
        Test delete_mibs_for_user when its used to delete all mibs when the user has two mibs
        '''
        self.create_message()
        self.create_message(message_id=test_message_id2)
        with self.app.app_context():
            self.assertTrue(delete_mibs_for_user(test_user_id, None))
            self.assertEqual(None, Message.query.get(test_message_id))
            self.assertEqual(None, Message.query.get(test_message_id2))

    def test_delete_mibs_for_user_specific_no_mibs(self):
        '''
        Test delete_mibs_for_user when its used to delete a single mib when the user has no mibs
        '''
        with self.app.app_context():
            self.assertFalse(delete_mibs_for_user(test_user_id, test_message_id))
            self.assertEqual(None, Message.query.get(test_message_id))

    def test_delete_mibs_for_user__specific_no_mibs_but_another_user_has_a_mib(self):
        '''
        Test delete_mibs_for_user when its used to delete a single mib when the user has no mibs
        but another user has a mib
        '''
        self.create_message(user_id=test_other_user)
        with self.app.app_context():
            self.assertFalse(delete_mibs_for_user(test_user_id, test_message_id))
            self.assertNotEqual(None, Message.query.get(test_message_id))

    def test_delete_mibs_for_user_specific_one_mib(self):
        '''
        Test delete_mibs_for_user when its used to delete a single mib when the user has one mib
        '''
        self.create_message()
        with self.app.app_context():
            self.assertTrue(delete_mibs_for_user(test_user_id, test_message_id))
            self.assertEqual(None, Message.query.get(test_message_id))

    def test_delete_mibs_for_user_specific_two_mibs(self):
        '''
        Test delete_mibs_for_user when its used to delete a single mib when the user has two mibs
        '''
        self.create_message()
        self.create_message(message_id=test_message_id2)
        with self.app.app_context():
            self.assertTrue(delete_mibs_for_user(test_user_id, test_message_id))
            self.assertEqual(None, Message.query.get(test_message_id))
            self.assertNotEqual(None, Message.query.get(test_message_id2))

    def test_delete_all_no_mibs(self):
        '''
        Test DELETE /mibs to delete all mibs when user has no mibs
        '''
        with self.app.app_context():
            response = self.client.delete('/mibs',
                headers={'Authorization': 'Bearer ' + self.get_token()})
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual('Failed to delete all mibs: User does not have any mibs',
                         response.get_data(as_text=True))
        self.assertEqual(0, self.get_num_user_messages())

    def test_delete_all_no_mibs_but_another_user_has_a_mib(self):
        '''
        Test DELETE /mibs to delete all mibs when user has no mibs but another user has a mib
        '''
        self.create_message(user_id=test_other_user)
        with self.app.app_context():
            response = self.client.delete('/mibs',
                headers={'Authorization': 'Bearer ' + self.get_token()})
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual('Failed to delete all mibs: User does not have any mibs',
                         response.get_data(as_text=True))
        self.assertEqual(0, self.get_num_user_messages())
        self.assertEqual(1, self.get_num_user_messages(test_other_user))

    def test_delete_all_one_mib(self):
        '''
        Test DELETE /mibs to delete all mibs when user has one mib
        '''
        self.create_message()
        with self.app.app_context():
            response = self.client.delete('/mibs',
                headers={'Authorization': 'Bearer ' + self.get_token()})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('Successfully deleted all mibs',
                         response.get_data(as_text=True))
        self.assertEqual(0, self.get_num_user_messages())

    def test_delete_all_two_mibs(self):
        '''
        Test DELETE /mibs to delete all mibs when user has two mibs
        '''
        self.create_message()
        self.create_message(message_id=test_message_id2)
        with self.app.app_context():
            response = self.client.delete('/mibs',
                headers={'Authorization': 'Bearer ' + self.get_token()})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('Successfully deleted all mibs',
                         response.get_data(as_text=True))
        self.assertEqual(0, self.get_num_user_messages())

    def test_delete_specific_no_mibs(self):
        '''
        Test DELETE /mibs to delete a specific mib when user has no mibs
        '''
        with self.app.app_context():
            response = self.client.delete(f'/mibs?messageId={test_message_id}',
                headers={'Authorization': 'Bearer ' + self.get_token()})
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual('Failed to delete mib with message id 1',
                         response.get_data(as_text=True))
        self.assertEqual(0, self.get_num_user_messages())

    def test_delete_specific_no_mibs_but_another_user_has_a_mib(self):
        '''
        Test DELETE /mibs to delete a specific mib when user has no mibs but another user has a
        mib
        '''
        self.create_message(user_id=test_other_user)
        with self.app.app_context():
            response = self.client.delete(f'/mibs?messageId={test_message_id}',
                headers={'Authorization': 'Bearer ' + self.get_token()})
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual('Failed to delete mib with message id 1',
                         response.get_data(as_text=True))
        self.assertEqual(0, self.get_num_user_messages())
        self.assertEqual(1, self.get_num_user_messages(test_other_user))

    def test_delete_specific_mib_when_user_has_one_mib(self):
        '''
        Test DELETE /mibs to delete a specific mib when user has one mib
        '''
        self.create_message()
        with self.app.app_context():
            response = self.client.delete(f'/mibs?messageId={test_message_id}',
                headers={'Authorization': 'Bearer ' + self.get_token()})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('Successfully deleted mib with message id 1',
                         response.get_data(as_text=True))
        self.assertEqual(0, self.get_num_user_messages())

    def test_delete_invalid_mib_id_when_user_has_no_mib(self):
        '''
        Test DELETE /mibs with invalid messageId when when user has no mib
        '''
        invalid_message_id= 'helloUniverse'
        with self.app.app_context():
            response = self.client.delete(f'/mibs?messageId={invalid_message_id}',
                headers={'Authorization': 'Bearer ' + self.get_token()})
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual('Invalid messageId',
                         response.get_data(as_text=True))
        self.assertEqual(0, self.get_num_user_messages())

    def test_delete_invalid_mib_id_when_user_has_one_mib(self):
        '''
        Test DELETE /mibs with invalid messageId when when user has one mib
        '''
        self.create_message()
        invalid_message_id= 'helloUniverse'
        with self.app.app_context():
            response = self.client.delete(f'/mibs?messageId={invalid_message_id}',
                headers={'Authorization': 'Bearer ' + self.get_token()})
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual('Invalid messageId',
                         response.get_data(as_text=True))
        self.assertEqual(1, self.get_num_user_messages())

    def test_delete_invalid_mib_id_when_user_has_two_mibs(self):
        '''
        Test DELETE /mibs with invalid messageId when when user has two mibs
        '''
        self.create_message()
        self.create_message(message_id=2)
        invalid_message_id= 'helloUniverse'
        with self.app.app_context():
            response = self.client.delete(f'/mibs?messageId={invalid_message_id}',
                headers={'Authorization': 'Bearer ' + self.get_token()})
        self.assertEqual(HTTPStatus.BAD_REQUEST, response.status_code)
        self.assertEqual('Invalid messageId',
                         response.get_data(as_text=True))
        self.assertEqual(2, self.get_num_user_messages())

    def test_delete_specific_mib_when_user_has_two_mibs(self):
        '''
        Test DELETE /mibs to delete a specific mib when user has two mibs
        '''
        self.create_message()
        self.create_message(message_id=2)
        with self.app.app_context():
            response = self.client.delete(f'/mibs?messageId={test_message_id}',
                headers={'Authorization': 'Bearer ' + self.get_token()})
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('Successfully deleted mib with message id 1',
                         response.get_data(as_text=True))
        self.assertEqual(1, self.get_num_user_messages())

    def test_delete_mib_also_deletes_email_recipients(self):
        '''
        Test when deleting a mib, that any email recipients associated with the message are also
        automatically deleted
        '''
        self.create_message()
        with self.app.app_context():
            self.create_email_recipient()
            self.create_email_recipient(message_send_request_id=2)
            delete_mibs_for_user(test_user_id, test_message_id)
            self.assertEqual(None, EmailMessageRecipient.query.get(1))
            self.assertEqual(None, EmailMessageRecipient.query.get(2))

    def test_get_no_mibs_exist_id(self):
        '''
        Test GET /mibs using a given messageId on an empty database
        '''
        response = self.client.get('/mibs?messageId=1',
            headers={'Authorization': 'Bearer ' + self.get_token()})
        status = response.status_code
        data = response.get_json()
        self.assertEqual(data, [])
        self.assertEqual(status, HTTPStatus.NOT_FOUND)

    def test_get_no_mibs_exist_no_id(self):
        '''
        Test GET /mibs with no given messageId on an empty database
        '''
        response = self.client.get('/mibs',
            headers={'Authorization': 'Bearer ' + self.get_token()})
        status = response.status_code
        data = response.get_json()
        self.assertEqual(data, [])
        self.assertEqual(status, HTTPStatus.OK)

    def test_get_request_with_nonexistant_id(self):
        '''
        Testing GET /mibs to try retrieving a mib with an non-existant messageId
        '''
        self.populate_messages()
        response = self.client.get('/mibs?messageId=100',
            headers={'Authorization': 'Bearer ' + self.get_token()})
        status = response.status_code
        data = response.get_json()
        self.assertEqual(data, [])
        self.assertEqual(status, HTTPStatus.NOT_FOUND)

    def test_get_mib_with_valid_id(self):
        '''
        Test GET /mibs to try retrieving a mib with an existant messageId
        '''
        self.populate_messages()
        response = self.client.get('/mibs?messageId=1',
            headers={'Authorization': 'Bearer ' + self.get_token()})
        status = response.status_code
        data = response.get_json()
        self.assertNotEqual(data, [])
        self.assertEqual(data[0]['message_id'], 1)
        self.assertEqual(status, HTTPStatus.OK)

    def test_get_request_with_invalid_id(self):
        '''
        Testing GET /mibs to try retrieving a mib with an invalid messageId
        '''
        self.populate_messages()
        response = self.client.get('/mibs?messageId=helloWorld',
         headers={'Authorization': 'Bearer ' + self.get_token()})
        status = response.status_code
        data = response.data
        self.assertEqual(data, b'invalid messageId: messageId must be an integer')
        self.assertEqual(status, HTTPStatus.BAD_REQUEST)

    def test_get_no_given_message_id(self):
        '''
        Test when no messageId is given
        '''
        self.populate_messages()
        response = self.client.get('/mibs',
            headers={'Authorization': 'Bearer ' + self.get_token()})
        status = response.status_code
        data = response.get_json()
        self.assertIsNotNone(data)
        self.assertEqual(len(data), 5)
        self.assertEqual(data[0]['message_id'], 1)
        self.assertEqual(data[0]['message'], 'This was my first mibs message!')
        self.assertEqual(data[0]['recipients'][0]['email'], 'test@mail')
        self.assertEqual(data[1]['message_id'], 2)
        self.assertEqual(data[2]['message_id'], 5)
        self.assertEqual(data[3]['message_id'], 6)
        self.assertEqual(data[4]['message_id'], 9)
        self.assertEqual(status, HTTPStatus.OK)


    def create_email_recipient(self,
                               message_send_request_id=1,
                               message_id=test_message_id,
                               email=test_email):
        '''
        Helper function to create and insert a email recipient in the database
        '''
        with self.app.app_context():
            email_recipient = EmailMessageRecipient(message_send_request_id=message_send_request_id,
                message_id=message_id,
                email=email)
            db.session.add(email_recipient)
            db.session.commit()


    def create_message(self,
        message_id=test_message_id,
        user_id=test_user_id,
        message='test',
        send_time=datetime.now()):
        '''
        Helper function to create and insert a message in the database
        '''
        with self.app.app_context():
            new_message = Message(message_id=message_id,
                user_id=user_id,
                message=message,
                send_time=send_time)
            db.session.add(new_message)
            db.session.commit()

    def get_num_user_messages(self, user_id=test_user_id):
        '''
        Helper function to get the number of messages a user has in the database
        '''
        with self.app.app_context():
            return db.session.query(Message).filter(Message.user_id == user_id).count()

    def populate_messages(self):
        filler_mibs = [
            {'message_id': 1, 'user_id': 'test-user',
                'message': 'This was my first mibs message!',
                'recipients': [{'email': 'test@mail'}],
                'send_time': '2021-10-27T23:22:19.911Z'},
            {'message_id': 2, 'user_id': 'test-user',
                'message': 'This was my second mibs message!',
                'recipients': [{'email': 'test2@mail'}],
                'send_time': '2021-10-27T23:22:19.911Z'},
            {'message_id': 3, 'user_id': 'some id',
                'message': 'This is someone elses message!',
                'recipients': [{'email': 'test3@mail'}],
                'send_time': '2021-10-27T23:22:19.911Z'},
            {'message_id': 4, 'user_id': 'a third id',
                'message': 'There are more people making messages!',
                'recipients': [{'email': 'test4@mail'}, {'email': 'aSecond@email'}],
                'send_time': '2021-10-27T23:22:19.911Z'},
            {'message_id': 5, 'user_id': 'test-user',
                'message': 'This is actually my third message (ignore the 5)!',
                'recipients': [{'email': 'test5@mail'}],
                'send_time': '2021-10-27T23:22:19.911Z'},
            {'message_id': 6, 'user_id': 'test-user',
                'message': 'I have a lot of messages!',
                'recipients': [{'email': 'test6@mail'}],
                'send_time': '2021-10-27T23:22:19.911Z'},
            {'message_id': 7, 'user_id': 'a third id',
                'message': 'Felt like I needed another message!',
                'recipients': [{'email': 'test7@mail'}],
                'send_time': '2021-10-27T23:22:19.911Z'},
            {'message_id': 8, 'user_id': 'some id',
                'message': 'Me too!',
                'recipients': [{'email': 'randomemail@mail'}],
                'send_time': '2021-10-27T23:22:19.911Z'},
            {'message_id': 9, 'user_id': 'test-user',
                'message': 'We are almost up to ten mibs in the db!',
                'recipients': [{'email': 'test9@mail'}],
                'send_time': '2021-10-27T23:22:19.911Z'}
        ]
        with self.app.app_context():
            for i in range(len(filler_mibs)):
                recipients = [EmailMessageRecipient(email=r['email'])
                    for r in filler_mibs[i]['recipients']]
                db.session.add(Message(message_id=filler_mibs[i]['message_id'],
                                       user_id=filler_mibs[i]['user_id'],
                                       message=filler_mibs[i]['message'],
                                       email_recipients=recipients,
                                       send_time=datetime.now()))
            db.session.commit()


    def get_token(self, is_valid=True):
        if is_valid:
            headers = {'alg': 'RS256', 'typ': 'JWT', 'kid': '0'}
            payload = {
                'iss': 'test_issuer',
                'exp': int(time.time()) + 30,
                'aud': 'test',
                'sub': 'test-user',
            }
            access_token = jwt.encode(payload, private_pem,
                algorithm='RS256',
                headers=headers
            )
        else:
            access_token = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMj'
                'M0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTU'
                'xNjIzOTAyMn0.NHVaYe26MbtOYhSKkoKYdFVomg4i8ZJd8_-RU8VNbftc4TSMb4bX'
                'P3l3YlNWACwyXPGffz5aXHc6lty1Y2t4SWRqGteragsVdZufDn5BlnJl9pdR_kdVF'
                'Usra2rWKEofkZeIC4yWytE58sMIihvo9H1ScmmVwBcQP6XETqYd0aSHp1gOa9RdUP'
                'DvoXQ5oqygTqVtxaDr6wUFKrKItgBMzWIdNZ6y7O9E0DhEPTbE9rfBo6KTFsHAZnM'
                'g4k68CDp2woYIaXbmYTWcvbzIuHO7_37GT79XdIwkm95QJ7hYC9RiwrV7mesbY4PA'
                'ahERJawntho0my942XheVLmGwLMBkQ')
        return access_token


if __name__ == '__main__':
    unittest.main()

'''
/mibs endpoint unit tests
'''

import unittest

import re
from urllib.parse import urlparse, parse_qs
from dateutil.parser import parse as datetimeParse
from datetime import  datetime
from api.mibs import mibs_blueprint, delete_mibs_for_user, TEMP_USER_ID
from models import Message, EmailMessageRecipient, db
from flask import Flask
from http import HTTPStatus

test_email = 'test@email.com'
test_user_id = 'temp-user-id'
test_other_user = 'other_user'
test_message_id = 1
test_message_id2 = 2


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
            json=self.test_post_message
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'Request is not JSON')

    def test_post_missing_message(self):
        '''
        Test POST /mibs when request body is missing field "message"
        '''
        self.test_post_message.pop('message')
        response = self.client.post(
            '/mibs',
            json=self.test_post_message
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
            json=self.test_post_message
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
            json=self.test_post_message
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'Must have atleast 1 recipient')

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
            json=self.test_post_message
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
            json=self.test_post_message
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
            json=self.test_post_message
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'"sendTime" is not an ISO-8601 UTC date time string')

    def test_post_success_1_recipient(self):
        '''
        Test POST /mibs when request is successful with one recipient
        '''
        response = self.client.post(
            '/mibs',
            json=self.test_post_message
        )

        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        self.assertIn('Location', response.headers)
        self.assertRegex(response.headers['Location'], re.compile(r'^.*/mibs\?messageId=\d+$'))
        self.assertEqual(response.data, b'MessageInABottle was successfully created')

        message_id = int(parse_qs(urlparse(response.headers['Location']).query)['messageId'][0])

        with self.app.app_context():
            message = Message.query.get(message_id)

            self.assertEqual(message.message_id, message_id)
            self.assertEqual(message.user_id, TEMP_USER_ID)
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
            json=self.test_post_message
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
            json=self.test_put_message
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
            json=self.test_put_message
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
            json=self.test_put_message
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
            json=self.test_put_message
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
            json=self.test_put_message
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'Must have atleast 1 recipient')

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
            json=self.test_put_message
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
            json=self.test_put_message
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
            json=self.test_put_message
        )

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response.data, b'"sendTime" is not an ISO-8601 UTC date time string')

    def test_put_no_message_in_database(self):
        '''
        Test PUT /mibs when the messageId does not exist in the database
        '''
        response = self.client.put(
            '/mibs',
            json=self.test_put_message
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
            json=self.test_put_message
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
            json=self.test_put_message
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
            json=self.test_put_message
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn('Location', response.headers)
        self.assertEqual(response.data, b'MessageInABottle was successfully updated')

        with self.app.app_context():
            message = Message.query.get(self.test_put_message['messageId'])

            self.assertEqual(message.message_id, self.test_put_message['messageId'])
            self.assertEqual(message.user_id, TEMP_USER_ID)
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
            json=self.test_put_message
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
            json=self.test_put_message
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
            response = self.client.delete('/mibs')
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
            response = self.client.delete('/mibs')
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
            response = self.client.delete('/mibs')
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
            response = self.client.delete('/mibs')
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('Successfully deleted all mibs',
                         response.get_data(as_text=True))
        self.assertEqual(0, self.get_num_user_messages())

    def test_delete_specific_no_mibs(self):
        '''
        Test DELETE /mibs to delete a specific mib when user has no mibs
        '''
        with self.app.app_context():
            response = self.client.delete(f'/mibs?messageId={test_message_id}')
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
            response = self.client.delete(f'/mibs?messageId={test_message_id}')
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
            response = self.client.delete(f'/mibs?messageId={test_message_id}')
        self.assertEqual(HTTPStatus.OK, response.status_code)
        self.assertEqual('Successfully deleted mib with message id 1',
                         response.get_data(as_text=True))
        self.assertEqual(0, self.get_num_user_messages())

    def test_delete_specific_mib_when_user_has_two_mibs(self):
        '''
        Test DELETE /mibs to delete a specific mib when user has two mibs
        '''
        self.create_message()
        self.create_message(message_id=2)
        with self.app.app_context():
            response = self.client.delete(f'/mibs?messageId={test_message_id}')
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


if __name__ == '__main__':
    unittest.main()

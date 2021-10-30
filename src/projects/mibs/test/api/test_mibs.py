"""
Stub for MIBS system
"""
import unittest
from flask import Flask, request
from models import db, Message
from api.mibs import mibs_blueprint
from flask import HTTPStatus
from datetime import datetime

# mibs to populate the db
filler_mibs = [
    {"message_id": 1, "user_id": 1,
        "message": "This was my first mibs message!",
        "send_time": datetime.now()},
    {"message_id": 2, "user_id": 1,
        "message": "This was my second mibs message!",
        "send_time": datetime.now()},
    {"message_id": 3, "user_id": 2,
        "message": "This is someone else's message!",
        "send_time": datetime.now()},
    {"message_id": 4, "user_id": 3,
        "message": "There are more people making messages!",
        "send_time": datetime.now()},
    {"message_id": 5, "user_id": 1,
        "message": "This is actually my third message (ignore the 5)!",
        "send_time": datetime.now()},
    {"message_id": 6, "user_id": 1,
        "message": "I have a lot of messages!",
        "send_time": datetime.now()},
    {"message_id": 7, "user_id": 3,
        "message": "Felt like I needed another message!",
        "send_time": datetime.now()},
    {"message_id": 8, "user_id": 2,
        "message": "Me too!",
        "send_time": datetime.now()},
    {"message_id": 9, "user_id": 1,
        "message": "We are almost up to ten mibs in the db!",
        "send_time": datetime.now()}
]


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

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_no_mibs_exist_id(self):
        """
        mibs-GET
        Trying to retrieve mibs on an empty database giving a messageId
        Expected outcome: None is returned with NOT_FOUND response
        """
        response = self.client.get("/mibs", json={"messageId": 1})
        self.assertIsNone(response.data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_no_mibs_exist_no_id(self):
        """
        mibs-GET
        Trying to retrieve mibs on an empty database without giving a messageId
        Expected outcome: None is returned with OK response
        """
        response = self.client.get("/mibs", json={"messageId": None})
        self.assertIsNone(response.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_request_with_nonexistant_id_(self):
        """
        mibs-GET
        Searching for MIB with a messageId that does not exist
        Expected outcome: all MIBS for the user are returned with a NOT_FOUND
        response
        """
        self.populate_messages()
        response = self.client.get("/mibs", json={"messageId": 100})
        self.assertIsNone(response.data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_get_mib_with_valid_id(self):
        """
        mibs-GET
        Searching for a MIB with a valid messageId
        Expected outcome: the MIB with the corresponding messageId is returned with
        an OKAY response
        """
        response = self.client.get("/mibs", json={"messageId": 1})
        self.assertEqual(response.data["message_id"], 1)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_no_given_message_id(self):
        """
        mibs-GET
        Making request with no given messageId
        Expected outcome: all MIBs for the user are returned with an OKAY response
        """
        response = self.client.get("/mibs", json={"messageId": None})
        self.assertIsNotNone(response.data)
        # user should have 5 messages
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # def not_authorized(self):
    #     """
    #     mibs-GET
    #     Making a request from an unauthorized user
    #     Expected outcome: no Mibs are returned with an UNAUTHORIZED response
    #     """
    #     pass

    def populate_messages():
        """
        Fills database with messages
        """
        for i in range(len(filler_mibs)):
            db.session.add(Message(message_id=filler_mibs[i]["message_id"],
                                   user_id=filler_mibs[i]["user_id"],
                                   message=filler_mibs[i]["message"],
                                   send_time=filler_mibs[i]["send_time"]))
        db.session.commit()


if __name__ == '__main__':
    unittest.main()

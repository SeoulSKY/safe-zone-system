# import unittest

# from sqlalchemy.sql.expression import true
# from api.mibs import mibs_blueprint, delete_mibs_for_user, TEMP_USER_ID
# from models import Message, EmailMessageRecipient, db
# from lib.mibs.python.openapi.swagger_server.models import MessageInABottle, EmailRecipient
# from flask import Flask
# from services.message_pool_service import MessagePoolingService
# from datetime import timedelta, datetime

# TEMP_USER_ID = 'temp-user-id'
# TEST_EMAIL_DOMAIN = '.message_pool_service@email.com'
# class TestEmailService(unittest.TestCase):

#     def setUp(self):
#         self.app = Flask(__name__)
#         self.app.config['TESTING'] = True
#         db.init_app(self.app)
#         with self.app.app_context():
#             db.create_all()
#             db.engine.execute('PRAGMA foreign_keys=ON')
#         self.app.register_blueprint(mibs_blueprint)
#         self.client = self.app.test_client()
#         self.email_recipients = []
#         self.mibs = []
#         self.last_week = (datetime.utcnow - timedelta(weeks=1))
#         self.add_mibs()

#     def add_mibs(self):
#         for i in range(1, 10):
#             email_recipient =  EmailRecipient("testuser"+i+TEST_EMAIL_DOMAIN)
#             self.email_recipients.append(email_recipient)
#             message = Message(
#                 user_id=TEMP_USER_ID,
#                 message="Test message for user" + i,
#                 send_time=self.last_week,
#                 email_recipients=[email_recipient]
#             )
#             self.mibs.append(message)
#             db.session.add(message)
#         db.session.commit()

#     def tearDown(self):
#         with self.app.app_context():
#             db.session.remove()
#             db.drop_all()

#     def test__update_recipients_send_attempt_time(self):
#         message_pool_service = MessagePoolingService()
#         message_pool_service._update_recipients_send_attempt_time(None)
#         email_recipients = EmailMessageRecipient.query.all()
#         for recipient in email_recipients:
#             self.assertEqual(recipient.send_attempt_time, self.last_week)

#         message_pool_service._update_recipients_send_attempt_time(self.email_recipients)
#         email_recipients = EmailMessageRecipient.query.all()
#         for recipient in email_recipients:
#             self.assertEqual(recipient.send_attempt_time, message_pool_service._current_time)

#     def test_get_mib_with_email_recipients(self):
#         message_pool_service = MessagePoolingService()

#         test_user1_mib = MessageInABottle(message_id=self.user1["messageId"],
#             message=self.user1["message"],send_time=self.user1["sendTime"],
#             recipients=[EmailRecipient(email=recipient.email)
#                 for recipient in self.user1["recipients"]]).to_dict()

#         mib = (self.user1["messageId"], self.user1["message"], self.user1["sendTime"])
#         result_mib = message_pool_service._get_mib_with_email_recipients(mib)

#     def test_get_mib_with_email_recipients(self):
#         message_pool_service = MessagePoolingService()
#         test_mib = self.mib[0]
#         test_mib_tuple = (test_mib.user_id, test_mib.message, test_mib.send_time)
#         result_mib = message_pool_service._get_mib_with_email_recipients(test_mib_tuple)
#         self.assertDictEqual(result_mib, test_mib)

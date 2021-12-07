import unittest

from api.mibs import mibs_blueprint, delete_mibs_for_user
from models import Message, EmailMessageRecipient, db
from lib.mibs.python.openapi.swagger_server.models import MessageInABottle, EmailRecipient
from flask import Flask
from services.message_pool_service import MessagePoolingService
from datetime import timedelta, datetime
from lib.logger.safezone_logger import get_logger

LOGGER = get_logger(__name__)
TEMP_USER_ID='temp-user-id'
TEST_EMAIL_DOMAIN = '.message_pool_service@email.com'
class TestEmailService(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            db.engine.execute('PRAGMA foreign_keys=ON')
        self.app.register_blueprint(mibs_blueprint)
        self.client = self.app.test_client()
        self.mibs = []
        self.last_week = (datetime.utcnow() - timedelta(weeks=1))
        LOGGER.debug(self.mibs)
        self.add_mibs()

    def add_mibs(self):
        with self.app.app_context():
            for i in range(1, 5):
                email_recipients = [EmailMessageRecipient(
                    email=f"recipient{j}.testuser{i}{TEST_EMAIL_DOMAIN}") for j in range(3)]
                message = Message(
                    user_id=TEMP_USER_ID,
                    message=f"Test message for user{i}",
                    send_time=self.last_week,
                    email_recipients=email_recipients)
                self.mibs.append(message)
                db.session.add(message)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test__update_recipients_send_attempt_time(self):
        with self.app.app_context():
            email_recipients_preupdate = EmailMessageRecipient.query.all()
            message_pool_service = MessagePoolingService()
            message_pool_service._update_recipients_send_attempt_time(email_recipients_preupdate)

            email_recipients_postupdate =  EmailMessageRecipient.query.all()
            for recipient in email_recipients_postupdate:
                self.assertNotEqual(recipient.send_attempt_time, self.last_week)
                self.assertEqual(recipient.send_attempt_time, message_pool_service._current_time)

if __name__ == '__main__':
    unittest.main()
"""
Messaging Service responsible for introspecting mibs DB and sending unsent messages to the 
email service
"""
import time 
from datetime import timedelta
from datetime import datetime
from threading import Thread

from models import Message, EmailMessageRecipient, db
from lib.mibs.python.openapi.swagger_server.models import MessageInABottle, EmailRecipient
from services.email_sender import email_service

class message_pooler:
    '''
    Class responsible for pooling, updating DB and calling email service
    '''
    def __init__(self):

        self._POOL_INTERVAL = 305 #seconds
        self._MSG_TIME_THRESHOLD = timedelta(minutes=5)
        self._current_time = datetime.utcnow()
        self._list_of_messages = []
        self._email_sender = email_service()

        # Thread.__init__(self)
        # self.daemon = True
        
    def run(self):
        for i in range(3):
            print("Running...%d", i)
            self.get_mibs()
            time.sleep(self._POOL_INTERVAL)

    def get_mibs(self):

        self._current_time = datetime.utcnow()
        time_difference = self._current_time - self._MSG_TIME_THRESHOLD
        print(time_difference)

        # want to call update and use updated rows for next phase
        mibs = Message.query.\
            filter(Message.last_sent_time <= time_difference, Message.sent == False).all()
        for mib in mibs:
            mib.last_sent_time = self._current_time
            self.update_recipient_send_attempt_time(mib.email_recipients)
            self._list_of_messages.append(
                MessageInABottle(message_id=mib.message_id,
                message=mib.message,send_time=mib.send_time,
                recipients=[EmailRecipient(email=recipient.email)
                    for recipient in mib.email_recipients]).to_dict())

        db.session.commit()
        self._email_sender.send_email(self._list_of_messages)

    def update_recipient_send_attempt_time(self, email_recipients):
        for recipient in email_recipients:
                recipient.send_attempt_time = self._current_time
                db.session.add(recipient)

        # N/B : For updating, we could use this and then fetch from table, 
        # but table would already be updated
        # number_of_rows_updated = \
        #     Message.query.filter(Message.last_sent_time <= time_difference).\
        #     update({"last_sent_time": current_time}, synchronize_session=False)

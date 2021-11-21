"""
Messaging Service responsible for introspecting mibs DB and sending unsent messages to the 
email service
"""
import time 
import sqlalchemy
from multiprocessing import Process
from datetime import timedelta, datetime
from models import Message, db
from lib.mibs.python.openapi.swagger_server.models import MessageInABottle, EmailRecipient
from projects.mibs.src.models import EmailMessageRecipient
from services.email_sender import email_service

class message_service(Process):
    '''
    Class responsible for pooling, updating DB and calling email service
    '''
    # use process not threads
    def __init__(self):
        super(message_service, self).__init__()
        self._POOL_INTERVAL = 30.0 #seconds
        self._MSG_TIME_THRESHOLD = timedelta(minutes=1)
        self._current_time = datetime.utcnow()
        self._email_sender = email_service()
        self.cancelled = False

    def run(self):
        ''' Begin thread operation '''
        while not self.cancelled:
            print('Pooling unsent messages...')
            self.get_unsent_mibs()
            time.sleep(self._POOL_INTERVAL)

    def cancel(self):
        ''' End the thread '''
        self.cancelled = True

    def get_unsent_mibs(self):

        self._current_time = datetime.utcnow()
        time_difference = self._current_time - self._MSG_TIME_THRESHOLD
        print(time_difference)

        updated_mibs = db.session.execute(sqlalchemy.text('UPDATE public."Message" SET "lastSentTime" = :current_time WHERE "lastSentTime" <= :time_diff AND "sent" = \'false\' \
            RETURNING "messageId","message", "sendTime"'),\
            {'current_time': self._current_time, 'time_diff':time_difference})
        
        for mib in updated_mibs:
            print(mib)
            mib_message_id = mib[0]
            mib_message = mib[1]
            mib_send_time = mib[2]
            mib_email_recipient_list = self.get_email_recipients(mib_message_id, mib_message, mib_send_time)

            all_emails_sent = self._email_sender.send_email(mib_email_recipient_list)
            if all_emails_sent is True:
                Message.query.filter(Message.sent == False, Message.last_sent_time == self._current_time).\
                    update({"sent": True}, synchronize_session=False)

    def get_email_recipients(self, mib_message_id, mib_message, mib_send_time):
        mib_recipients = EmailMessageRecipient.query().filter(EmailMessageRecipient.message_id == mib_message_id)
        self.update_recipient_send_attempt_time(mib_recipients)
        mibs_email_recipient_list = []
        mibs_email_recipient_list.append(
            MessageInABottle(message_id=mib_message_id,
            message=mib_message,send_time=mib_send_time,
            recipients=[EmailRecipient(email=recipient.email)
                for recipient in mib_recipients]).to_dict())
                
        return mibs_email_recipient_list

    def update_recipient_send_attempt_time(self, email_recipients):
        for recipient in email_recipients:
                recipient.send_attempt_time = self._current_time
                db.session.add(recipient)
        db.session.commit()

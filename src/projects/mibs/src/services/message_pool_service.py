"""
Messaging Service responsible for introspecting mibs DB and sending unsent messages to the
email service
"""
import time
import sqlalchemy
from multiprocessing import Process
from datetime import timedelta, datetime
from models import Message, EmailMessageRecipient, db
from lib.mibs.python.openapi.swagger_server.models import MessageInABottle, EmailRecipient
from services.email_service import EmailService
from lib.logger.safezone_logger import get_logger

LOGGER = get_logger(__name__)
POLL_INTERVAL = 30.0
MESSAGE_AGE_LIMIT = timedelta(minutes=1)

class MessagePoolingService(Process):
    '''
    Class responsible for pooling, updating DB and calling email service
    '''
    # use process not threads - Flask requests hang when using a Thread
    def __init__(self):
        super().__init__()
        self._email_service = EmailService()
        self._current_time = datetime.utcnow()
        self._cancelled = False

    def run(self):
        ''' Begin thread operation '''
        while not self._cancelled:
            LOGGER.info('Pooling unsent messages...')
            self._get_unsent_mibs_older_than_message_age_limit()
            time.sleep(POLL_INTERVAL)

    def cancel(self):
        ''' End the thread '''
        self._cancelled = True

    def _get_unsent_mibs_older_than_message_age_limit(self):
        '''
        criteria: unsent messages older than the specified age limit
        Get unsent mibs that meet criteria
        Preconditions:
            function is called within POOL_INTERVAL duration
        Postcondition:
            send all mibs that meet criteria to email service
            and "sent" values if they are all successfully sent
        '''
        self._current_time = datetime.utcnow()
        message_age_limit_in_datetime = self._current_time - MESSAGE_AGE_LIMIT
        LOGGER.info(f"target_time => {message_age_limit_in_datetime}")

        updated_mibs = db.session.execute(sqlalchemy.text(
            'UPDATE public."Message" SET "lastSentTime" = :current_time \
            WHERE ("lastSentTime" <= :message_age_limit OR "lastSentTime" IS NULL) \
            AND "sent" = \'false\' AND "sendTime" <= :current_time \
            RETURNING "messageId","message", "sendTime", "sent"'),
            {'current_time': self._current_time, 'message_age_limit':message_age_limit_in_datetime})
        LOGGER.info("Fetching mibs that match criteria")
        for mib in updated_mibs:
            mib_with_email_recipients = self._get_mib_with_email_recipients(mib)
            if len(mib_with_email_recipients) > 0:
                message_id = mib_with_email_recipients['message_id']
                message = mib_with_email_recipients['message']
                recipients = mib_with_email_recipients['recipients']
                all_mib_emails_sent = self._email_service.send_email(
                    message_id, message, recipients)
                if all_mib_emails_sent is True:
                    LOGGER.debug(f'All emails for message with id: {message_id} have been sent sent')
                    LOGGER.info(self._current_time)
                    message = Message.query.get(message_id)
                    message.sent = True
                    db.session.add(message)
            db.session.commit()

    def _get_mib_with_email_recipients(self, mib):
        '''
            Populate mib object, call _update_recipients_send_attempt_time
            and return mib object
            Preconditions:
                mib is not None
            Postcondition:
                mib object is populated and is returned
        '''
        assert mib is not None
        mib_message_id = mib[0]
        mib_message = mib[1]
        mib_send_time = mib[2]
        mib_recipients = EmailMessageRecipient.query.filter(
            EmailMessageRecipient.message_id == mib_message_id)
        self._update_recipients_send_attempt_time(mib_recipients)
        mib = MessageInABottle(message_id=mib_message_id,
            message=mib_message,send_time=mib_send_time,
            recipients=[EmailRecipient(email=recipient.email)
                for recipient in mib_recipients]).to_dict()
        return mib

    def _update_recipients_send_attempt_time(self, email_recipients):
        '''
            Preconditions:
                email_recipients is not None
            Postcondition:
                send_attempt_time is updated for all given recipients
        '''
        assert email_recipients is not None
        LOGGER.info("Updating recipients send attempt time")
        for recipient in email_recipients:
            recipient.send_attempt_time = self._current_time
            db.session.add(recipient)
        db.session.commit()

        
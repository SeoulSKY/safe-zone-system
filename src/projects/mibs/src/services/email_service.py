"""
Email Service responsible for sending mib messages to their respective recipients
"""
import smtplib
from models import EmailMessageRecipient, db
from lib.logger.safezone_logger import get_logger

SMTP_HOST_PORT = 25
SMTP_HOST = 'smtp-dev'
SENDER = 'cmpt371team1@gmail.com'
LOGGER = get_logger(__name__)
class EmailService:
    '''
    Class is responsible for formulating and sending email
    '''
    def __init__(self):
        self._all_mibs_sent = True

    def send_email(self, message_id, message, recipients):
        '''
        get email and recipient attributes from mib object in list
        send email sequentially and update recipient.sent column to true
        '''
        for recipient in recipients:
            LOGGER.debug(f"messageid => {message_id}, message => {message}, recipients => {recipients}")
            assert len(message) > 0
            assert message_id is not None
            recipient_email_address = recipient['email']
            LOGGER.debug(f'Attempting to send email to {recipient_email_address}...')
            #TODO: use some template for email body
            email_body = f'Hello, \n{message}'
            email_subject = 'MIBS'
            email_content = f'Subject: {email_subject}\n\n{email_body}'

            with smtplib.SMTP(SMTP_HOST, SMTP_HOST_PORT) as server:
                try:
                    server.sendmail(SENDER, recipient_email_address , email_content)
                    recipient_obj = EmailMessageRecipient.query.filter(
                        EmailMessageRecipient.email == recipient_email_address).first()
                    recipient_obj.sent = True
                    db.session.add(recipient_obj)
                except smtplib.SMTPException:
                    self.all_mibs_sent = False
                    LOGGER.debug(f'Could not send message with id: {message_id} \
                        to {recipient_email_address}')
        db.session.commit()
        if (self._all_mibs_sent and len(recipients) > 0):
            return True
        return False

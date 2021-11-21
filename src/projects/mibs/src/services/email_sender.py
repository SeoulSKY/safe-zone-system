"""
Email Service responsible for sending mib messages to their respective recipients
"""
import smtplib
from flask import Flask
from models import Message, EmailMessageRecipient, db

app = Flask(__name__)

"""
to start testing mail server in terminal, use the following command:
python3 -m smtpd -c DebuggingServer -n localhost:1025
the terminal will then sit and listen for incoming messages
"""

class email_service:
    '''
    Class is responsible for formulating and sending email
    '''
    def __init__(self):
        self.sender = '371emailTestBot@gmail.com'
        self.password = 'thisistestbot371!'
        self.transmissions = 0
        self.successful_transmissions = 0
        
    def send_email(self, mib_with_recipients):
        '''
        get email and recipient attributes from mib object in list
        send email sequentially and update recipient.sent column to true
        '''
        print("Attempting to send email...")
        print(mib_with_recipients)
        recipients = mib_with_recipients["recipients"]
        self.transmissions = len(recipients)

        for recipient in recipients:
            recipient_email_address = recipient.email
            email_body = f'Hello, \n{mib_with_recipients["message"]}'
            email_subject = 'MIBS'
            email_content = f"Subject: {email_subject}\n\n{email_body}"
            
            try:
                # server.sendmail(self.sender, recipient_email_address, email_content)
                print(email_content)
                self.successful_transmissions += 1
                recipient_obj = EmailMessageRecipient.filter(EmailMessageRecipient.email == recipient_email_address)
                recipient_obj.sent = True
                db.session.add(recipient_obj)
            except smtplib.SMTPException:
                print(f'Could not send message with id: {mib_with_recipients["messageId"]} to {recipient_email_address}')

        db.session.commit()

            # with smtplib.SMTP("localhost", 25) as server:

            #     try:
            #         # server.sendmail(self.sender, recipient_email_address, email_content)
            #         print(email_content)
            #         self.successful_transmissions += ONE
            #         recipient_obj = EmailMessageRecipient.filter(EmailMessageRecipient.email == recipient_email_address)
            #         recipient_obj.sent = True
            #         db.session.add(recipient_obj)
            #     except smtplib.SMTPException:
            #         print('Could not send message with id: {mib.message_id} to {recipient_email_address}')
            #     finally:
            #         db.session.commit()

        if self.successful_transmissions == self.transmissions:
            #all recipients for mib got email
            return True
        return False

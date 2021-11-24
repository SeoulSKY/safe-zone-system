"""
Email Service responsible for sending mib messages to their respective recipients
"""
import smtplib
from flask import Flask
from models import EmailMessageRecipient, db

class email_service:
    '''
    Class is responsible for formulating and sending email
    '''
    def __init__(self):
        self.sender = 'cmpt371team1@gmail.com'
        self.transmissions = 0
        self.successful_transmissions = 0
        
    def send_email(self, mib_with_recipients):
        '''
        get email and recipient attributes from mib object in list
        send email sequentially and update recipient.sent column to true
        '''
        print("Attempting to send email...")
        recipients = mib_with_recipients["recipients"]
        self.transmissions = len(recipients)
 
        for recipient in recipients:
            recipient_email_address = recipient.email
            email_body = f'Hello, \n{mib_with_recipients["message"]}'
            email_subject = 'MIBS'
            email_content = f"Subject: {email_subject}\n\n{email_body}"

            with smtplib.SMTP("host.docker.internal", 25) as server:
                try:
                    server.sendmail(self.sender, "cmpt371team1@gmail.com", email_content)
                    self.successful_transmissions += 1
                    recipient_obj = EmailMessageRecipient.filter(EmailMessageRecipient.email == recipient_email_address)
                    recipient_obj.sent = True
                    db.session.add(recipient_obj)
                except smtplib.SMTPException:
                    print(f'Could not send message with id: {mib_with_recipients["messageId"]} to {recipient_email_address}')

        db.session.commit()

        if (self.successful_transmissions == self.transmissions) and (self.transmissions > 0):
            #all recipients for mib got email
            return True
        return False

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Message(db.Model):
    """
    Database model representing a message in a bottle.
    """
    __tablename__ = "Message"

    message_id = db.Column("messageId", db.Integer, primary_key=True)
    user_id = db.Column("userId", db.Unicode, nullable=False)
    message = db.Column("message", db.UnicodeText, nullable=False)
    send_time = db.Column("sendTime", db.DateTime, nullable=False)
    sent = db.Column("sent", db.Boolean, nullable=False, default=False)
    last_sent_time = db.Column("lastSentTime", db.DateTime)

    def __init__(self, 
        message_id: str, 
        message: str, 
        send_time: datetime, 
        sent: bool, 
        last_send_time: datetime
    ) -> None:
        self.message_id = message_id
        self.message = message
        self.send_time = send_time
        self.sent = sent
        self.last_sent_time = last_send_time
        

class EmailMessageRecipient(db.Model):
    """
    Database model for a recipient of a message in a bottle via email.
    """
    __tablename__ = "EmailMessageRecipient"
    
    message_send_request_id = db.Column("messageSendRequestId", db.Integer, primary_key=True)
    message_id = db.Column("messageId", db.Integer, db.ForeignKey('person.id'), nullable=False)
    email = db.Column("email", db.Unicode, nullable=False)
    sent = db.Column("sent", db.Boolean, nullable=False, default=False)
    send_attempt_time = db.Column("sendAttemptTime", db.DateTime)

    def __init__(self,
        message_id: int,
        email: str,
        sent: bool,
        send_attempt_time: datetime
    ) -> None:
        self.message_id = message_id
        self.email = email
        self.sent = sent
        self.send_attempt_time = send_attempt_time
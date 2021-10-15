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
    last_sent_time = db.Column("lastSentTime", db.DateTime, default=None)

    def __init__(self, 
        user_id: str, 
        message: str, 
        send_time: datetime, 
    ) -> None:
        self.user_id = user_id
        self.message = message
        self.send_time = send_time
        

class EmailMessageRecipient(db.Model):
    """
    Database model for a recipient of a message in a bottle via email.
    """
    __tablename__ = "EmailMessageRecipient"

    message_send_request_id = db.Column("messageSendRequestId", db.Integer, primary_key=True)
    message_id = db.Column("MessageId", db.Integer, db.ForeignKey("Message.messageId"), nullable=False)
    email = db.Column("email", db.Unicode, nullable=False)
    sent = db.Column("sent", db.Boolean, nullable=False, default=False)
    send_attempt_time = db.Column("sendAttemptTime", db.DateTime, default=None)

    def __init__(self,
        message_id: int,
        email: str,
    ) -> None:
        self.message_id = message_id
        self.email = email





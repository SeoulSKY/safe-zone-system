'''
/mibs GET POST PUT DELETE endpoints
'''

from typing import Any, Dict, List, Tuple, Union
from flask import Blueprint, json, request, jsonify
from flask.helpers import url_for
from dateutil.parser import parse as datetimeParse
from http import HTTPStatus

from lib.mibs.python.openapi.swagger_server.models import MessageInABottle, EmailRecipient
from lib.mibs.python.openapi.swagger_server.models.any_of_message_in_a_bottle_recipients_items \
    import AnyOfMessageInABottleRecipientsItems
from lib.mibs.python.openapi.swagger_server.models.sms_recipient import SmsRecipient
from lib.mibs.python.openapi.swagger_server.models.user_recipient import UserRecipient
from models import Message, EmailMessageRecipient, db

mibs_blueprint = Blueprint('mibs', __name__, url_prefix='/mibs')

TEMP_USER_ID = 'temp-user-id'


@mibs_blueprint.route('', methods=['GET'])
def get():
    def serialize(mibs):
        if len(mibs) == 0:
            return []
        messages = []
        for m in mibs:
            messages.append(MessageInABottle(message_id=m.message_id,
                                             message=m.message,
                                             recipients=m.email_recipients).to_dict())
        return messages

    assert request is not None
    req = request.get_json()

    # if no message_id is given, retrieve all mibs for user
    if req["messageId"] is None:
        return (jsonify(serialize(Message.query.filter_by(user_id=1).all())), HTTPStatus.OK)

    # message_id is given
    else:
        mib = Message.query.filter_by(
            user_id=1, message_id=req["messageId"]).all()

        # if there's no message with the id, return NOT_FOUND
        if len(mib) == 0:
            status = HTTPStatus.NOT_FOUND
        else:
            status = HTTPStatus.OK
        return (jsonify(serialize(mib)), status)


@mibs_blueprint.route('', methods=['POST'])
# TODO add authorization decorator
def post():
    '''
    /mibs POST endpoint. See openapi file.
    '''

    def validate() -> Tuple[bool, Tuple[str, HTTPStatus]]:
        if not request.is_json:
            return False, ('Request is not JSON', HTTPStatus.BAD_REQUEST)

        body = request.get_json()
        if not 'message' in body:
            return False, ('"message" missing from request body', HTTPStatus.BAD_REQUEST)

        if not 'recipients' in body:
            return False, ('"recipients" missing from request body', HTTPStatus.BAD_REQUEST)

        email_recipients, sms_recipients, user_recipients, unknown_recipients = \
            _parse_recipients(body['recipients'])
        if len(unknown_recipients) > 0:
            return False, (f'Unknown recipient types: {json.dumps(unknown_recipients)}',
                           HTTPStatus.BAD_REQUEST)

        if len(email_recipients + sms_recipients + user_recipients) <= 0:
            return False, ('Must have atleast 1 recipient', HTTPStatus.BAD_REQUEST)

        if not 'sendTime' in body:
            return False, ('"sendTime" missing from request body', HTTPStatus.BAD_REQUEST)

        try:
            datetimeParse(body['sendTime'])
        except ValueError:
            return False, ('"sendTime" is not an ISO-8601 UTC date time string',
                           HTTPStatus.BAD_REQUEST)

        return True, (None, None)

    assert request is not None

    is_valid_request, error_response = validate()

    if not is_valid_request:
        return error_response

    # Note: the request recipients is not converted to a
    # AnyOfMessageInABottleRecipients and is instead just a dict
    mib = MessageInABottle.from_dict(request.get_json())
    email_recipients, *_ = _parse_recipients(mib.recipients)

    message = Message(
        user_id=TEMP_USER_ID,
        message=mib.message,
        send_time=mib.send_time,
        email_recipients=[
            EmailMessageRecipient(email=email_recipient.email)
            for email_recipient in email_recipients
        ]
    )

    db.session.add(message)
    db.session.commit()

    return 'MessageInABottle was successfully created', HTTPStatus.OK, \
        {'Location': url_for('.get', messageId=message.message_id)}


def _parse_recipients(recipients: List[Union[AnyOfMessageInABottleRecipientsItems,
                                             Dict[str, Any]]]) -> Tuple[EmailRecipient, SmsRecipient, UserRecipient, Dict[str, Any]]:
    '''
    Parse a list recipeints in to their respective categories.

    Preconditions:
        recipients is not None
        recipients is a list

    Postconditions:
        returns a tuple of (email_recipients, sms_recipients, user_recipients, unknown_recipients)
            where each element of the tuple is a list of recipients corresponding to that
            category
        Note: sms_recipients and user_recipients will always be empty lists and their entries
            will be in unknown_recipients since sms and user recipients are not implemented.
    '''

    assert recipients is not None
    assert isinstance(recipients, List)

    email_recipients = []
    sms_recipients = []
    user_recipients = []
    unknown_recipients = []
    for recipient in recipients:
        if 'email' in recipient:
            email_recipients.append(EmailRecipient.from_dict(recipient))
        else:
            unknown_recipients.append(recipient)

    return (email_recipients, sms_recipients, user_recipients, unknown_recipients)


@mibs_blueprint.route('', methods=['PUT'])
def put():
    '''
    TODO implement PUT endpoint here
    '''
    return {
      'success': json.dumps(True),
      'message': 'Hello from PUT /mibs',
    }


@mibs_blueprint.route('', methods=['DELETE'])
# TODO: add decorator
def delete():
    '''
    /mibs DELETE endpoint. See openapi file.
    '''
    assert request is not None
    message_id_unparsed = request.args.get('messageId', None)

    message_id = None if message_id_unparsed is None else int(message_id_unparsed)
    user_id = TEMP_USER_ID

    status_code = HTTPStatus.OK

    if delete_mibs_for_user(user_id, message_id):
        if message_id is None:
            message = 'Successfully deleted all mibs'
        else:
            message = f'Successfully deleted mib with message id {message_id}'
    else:
        status_code = HTTPStatus.NOT_FOUND
        if message_id is None:
            message = 'Failed to delete all mibs: User does not have any mibs'
        else:
            message = f'Failed to delete mib with message id {message_id}'

    return message, status_code


def delete_mibs_for_user(user_id: str, message_id: Union[None, str] = None) -> bool:
    '''
    Deletes one or more messages in a bottle for a user from the database
    Arguments:
        user_id - the id of the user to delete the mibs for
        message_id - an optional parameter for the id of the message
    Preconditions:
        message_id is None or an integer
        user_id is not None,
        user_id is a string
        user_id is not an empty string
    Postconditions:
        If message_id is present, the message with that id will be deleted if it is present and
        belongs to the user with user_id.
        If message_id is absent, all messages for the the user with user_id will be deleted
    Returns:
        True if any messages were deleted, false otherwise
    '''
    assert message_id is None or isinstance(message_id, int)
    assert user_id != ''
    assert isinstance(user_id, str)
    assert user_id is not None

    query = Message.query.filter(Message.user_id == user_id)
    if message_id is not None:
        query = query.filter(Message.message_id == message_id)
    count = query.count()
    if count > 0:
        query.delete()
        db.session.commit()
        return True
    return False


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
    '''
    /mibs GET endpoint. See openapi file.
    '''
    def serialize(mibs):
        if len(mibs) == 0:
            return []
        messages = []
        for m in mibs:
            messages.append(MessageInABottle(message_id=m.message_id,
                message=m.message,
                recipients=[EmailRecipient(email=er.email)
                    for er in m.email_recipients]).to_dict())
        return messages

    def get_all_messages(user_id):
        return jsonify(serialize(Message.query.filter_by(user_id=user_id).all()))

    assert request is not None
    given_id = request.args.get('messageId')
    if given_id is None:
        return get_all_messages(TEMP_USER_ID), HTTPStatus.OK

    # message_id is given
    mib = Message.query.filter_by(
        user_id=TEMP_USER_ID, message_id=given_id).all()

    if len(mib) == 0:
        status = HTTPStatus.NOT_FOUND
    else:
        status = HTTPStatus.OK
    return jsonify(serialize(mib)), status


@mibs_blueprint.route('', methods=['POST'])
# TODO add authorization decorator
def post():
    '''
    /mibs POST endpoint. See openapi file.
    '''
    return _handle_post_put(is_put=False)


def _handle_post_put(is_put=False):
    '''
    Handles /mibs POST and PUT endpoint

    Preconditions:
        is_put is a not None boolean
        The global request object is available with a POST or PUT request for /mibs

    Postcondition:
        see openapi file for /mibs PUT and POST endpoints
    '''

    def validate() -> Tuple[bool, Tuple[str, HTTPStatus], Message]:
        if not request.is_json:
            return False, ('Request is not JSON', HTTPStatus.BAD_REQUEST), None

        body = request.get_json()

        if is_put and not 'messageId' in body:
            return False, ('"messageId" missing from request body', HTTPStatus.BAD_REQUEST), None

        if not 'message' in body:
            return False, ('"message" missing from request body', HTTPStatus.BAD_REQUEST), None

        if not 'recipients' in body:
            return False, ('"recipients" missing from request body', HTTPStatus.BAD_REQUEST), None

        email_recipients, sms_recipients, user_recipients, unknown_recipients = \
            _parse_recipients(body['recipients'])
        if len(unknown_recipients) > 0:
            return False, (f'Unknown recipient types: {json.dumps(unknown_recipients)}', \
                HTTPStatus.BAD_REQUEST), None

        if len(email_recipients + sms_recipients + user_recipients) <= 0:
            return False, ('Must have atleast 1 recipient', HTTPStatus.BAD_REQUEST), None

        if not 'sendTime' in body:
            return False, ('"sendTime" missing from request body', HTTPStatus.BAD_REQUEST), None

        try:
            datetimeParse(body['sendTime'])
        except ValueError:
            return False, ('"sendTime" is not an ISO-8601 UTC date time string', \
                HTTPStatus.BAD_REQUEST), None

        message = None
        if is_put:
            message = Message.query \
                .filter_by(message_id=int(body['messageId']), user_id=TEMP_USER_ID).first()
            if message is None:
                return False, \
                    (f'a message with messageId={body["messageId"]} could not be found',
                    HTTPStatus.BAD_REQUEST), None

            if message.sent or message.last_sent_time is not None:
                return False, ('message already sent', HTTPStatus.BAD_REQUEST), None

        return True, (None, None), message

    assert request is not None
    assert isinstance(is_put, bool)

    is_valid_request, error_response, message = validate()

    if not is_valid_request:
        return error_response

    # Note: the request recipients is not converted to a
    # AnyOfMessageInABottleRecipients and is instead just a dict
    mib = MessageInABottle.from_dict(request.get_json())
    parsed_email_recipients, *_ = _parse_recipients(mib.recipients)
    email_recipients = [
        EmailMessageRecipient(email=email_recipient.email)
        for email_recipient in parsed_email_recipients
    ]

    if is_put:
        message.message = mib.message
        message.send_time = mib.send_time
        message.email_recipients = email_recipients

        db.session.commit()
        # call producer to send mib to topic
        return 'MessageInABottle was successfully updated', HTTPStatus.OK

    message = Message(
        user_id=TEMP_USER_ID,
        message=mib.message,
        send_time=mib.send_time,
        email_recipients=email_recipients
    )
    db.session.add(message)
    db.session.commit()

    return 'MessageInABottle was successfully created', HTTPStatus.CREATED, \
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
    /mibs PUT endpoint. See openapi file.
    '''
    return _handle_post_put(is_put=True)


@mibs_blueprint.route('', methods=['DELETE'])
# TODO: add decorator
def delete():
    '''
    /mibs DELETE endpoint. See openapi file.
    '''
    assert request is not None
    message_id_unparsed = request.args.get('messageId', None)

    message_id = None if message_id_unparsed is None else int(
        message_id_unparsed)
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

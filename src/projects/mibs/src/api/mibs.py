'''
/mibs GET POST PUT DELETE endpoints
'''

import Any, Dict, List, Tuple, Union
from flask import Blueprint, json, request
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


@mibs_blueprint.route('', methods=['GET'])
def get():
    assert request is not None
    id = request.args.get("messageId")

    # if no message_id is given, retrieve all mibs for user
    if id is None:
        return json.dumps(Message.filter_by(user_id=1)), HTTPStatus.OK

    # message_id is given
    else:
        mib = Message.filter_by(user_id=1, message_id=id).all()
        # no mib matching id, return nothing
        if mib is None:
            return "Message not found", HTTPStatus.NOT_FOUND
        else:
            return json.dumps(mib), HTTPStatus.OK


@mibs_blueprint.route('', methods=['POST'])
def post():
    '''
    TODO implement POST endpoint here
    '''
    return {
      'success': json.dumps(True),
      'message': 'Hello from POST /mibs',
    }


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
def delete():
    '''
    TODO implement DELETE endpoint here
    '''
    return {
      'success': json.dumps(True),
      'message': 'Hello from DELETE /mibs',
    }

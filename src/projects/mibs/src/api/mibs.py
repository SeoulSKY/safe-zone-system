'''
/mibs GET POST PUT DELETE endpoints
'''

from flask import Blueprint, json

mibs_blueprint = Blueprint('mibs', __name__, url_prefix='/mibs')

@mibs_blueprint.route('', methods=['GET'])
def get():
    '''
    TODO implement GET endpoint here
    '''
    return {
      'success': json.dumps(True),
      'message': 'Hello from GET /mibs',
    }


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

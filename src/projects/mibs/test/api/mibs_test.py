from ../src/api/mibs import get

"""
mibs-get
Searching for MIB with a messageId that does not exist
Expected outcome: all MIBS for the user are returned
"""


def nonexistant_id_messages():
    assert isinstance(json.loads(get(-1)).message, list)


"""
mibs-get
Searching for MIB with a messageId that does not exist
Expected outcome: a 404 response is returned
"""


def nonexistant_id_response():
    assert json.loads(get(-1)).success == 404


"""
mibs-get
Searching for a MIB with a valid messageId
Expected outcome: the MIB with the corresponding messageId is returned
"""


def valid_id_message():
    assert len(json.loads(get()).message) == 1


"""
mibs-get
Searching for a MIB with a valid messageId that
Expected outcome: a 200 response is returned
"""


def valid_id_response():
    assert json.loads(get()).success == 200


"""
mibs-get
Making request with no given messageId that
Expected outcome: all MIBs for the user are returned
"""


def no_given_id_message():
    pass


"""
mibs-get
Making request with no given messageId
Expected outcome: a 200 response is returned
"""


def no_given_id_response():
    assert json.load(get()).response == 200


"""
mibs-get
Making a request from an unauthorized user
Expected outcome: no Mibs are returned with a 401 response
"""


def not_authorized():
    assert json.loads(get()).response == 401


if __name__ == '__main__':
    print("*** Test Script Complete ***")

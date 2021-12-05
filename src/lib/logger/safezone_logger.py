"""
Safezone Logging Module
"""
import logging
from flask import has_request_context, request
from flask.logging import default_handler

class _RequestFormatter(logging.Formatter):
    '''
        Class for formatting reequests
    '''
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)

def get_logger(name):

    if name == None:
        print("Name is required")
        raise ValueError('A module name is required. Try get_logger(__name__)')

    logger = logging.getLogger(name)
    formatter = _RequestFormatter(
        '[%(asctime)s]: %(name)s - %(levelname)s\n \
            -- Remote Addr: %(remote_addr)s\n \
            -- URL: %(url)s\n \
            -- Message: %(message)s\n')
    default_handler.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(default_handler)

    return logger

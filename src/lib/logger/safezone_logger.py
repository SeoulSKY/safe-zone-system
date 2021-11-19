"""
Safezone Logging Module
"""
import logging

class _OneLineExceptionFormatter(logging.Formatter):
    '''
        Class for printing exceptions in single line
    '''
    def formatException(self, ei):
        '''
        Format an exception so that it prints on a single line.
        '''
        result = super().formatException(ei)
        return repr(result)

    def format(self, record):
        s = super().format(record)
        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s

def get_logger(name):

    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = _OneLineExceptionFormatter(
        '[%(asctime)s] %(name)s: - %(levelname)s \n>> %(message)s','%d/%m/%Y %H:%M'
    )
    handler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger

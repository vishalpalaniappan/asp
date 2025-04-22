import json
from MSG_TYPES import MSG_TYPES

def getMessageFromCode(code):
    '''
        Get the code description from the code.
    '''
    for key in MSG_TYPES:
        value = MSG_TYPES[key]
        if (value == code):
            return key        
    return "Unkown message code."
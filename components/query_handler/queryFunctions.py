import json
from SystemDatabaseReader import SystemDatabaseReader

reader = SystemDatabaseReader()

def handleUnknownMessage(message):
    '''
        Handle an unknown message.
    '''
    message["response"] = "Message does not contain a code"
    message["error"] = True
    return message

def handleGetSystems(message):
    '''
        Get all systems.
    '''
    response = reader.getSystems()

    if (response is None):
        message["error"] = True
        message["response"] = "An error occured while getting all systems."
    else:
        message["error"] = False
        message["response"] = response
        return message

def handleGetPrograms(message):
    '''
        Get all programs given a system version and id.
    '''
    data = message["data"]

    if ("systemId" not in data):
        message["response"] = "Request does not contain a system id."
        message["error"] = True
        return message

    if ("systemVersion" not in data):
        message["response"] = "Request does not contain a system version."
        message["error"] = True
        return message

    response = reader.getPrograms(
        systemId= message["data"]["systemId"],
        systemVersion= message["data"]["systemVersion"]
    )

    if (response is None):
        message["error"] = True
        message["response"] = "An error occured while getting programs."
    else:
        message["error"] = False
        message["response"] = response

    return message


def handleGetDeployments(message):
    '''
        Get all deployments given a system id and version.
    '''
    data = message["data"]

    if ("systemId" not in data):
        message["response"] = "Request does not contain a system id."
        message["error"] = True
        return message

    if ("systemVersion" not in data):
        message["response"] = "Request does not contain a system version."
        message["error"] = True
        return message

    response = reader.getDeployments(
        systemId= message["data"]["systemId"],
        systemVersion= message["data"]["systemVersion"]
    )

    if (response is None):
        message["error"] = True
        message["response"] = "An error occured while getting deployments."
    else:
        message["error"] = False
        message["response"] = response

    return message


def handleGetTraces(message):
    '''
        Get all traces given a system id, version and deployment id.
    '''
    data = message["data"]

    if ("systemId" not in data):
        message["response"] = "Request does not contain a system id."
        message["error"] = True
        return message

    if ("systemVersion" not in data):
        message["response"] = "Request does not contain a system version."
        message["error"] = True
        return message

    if ("deploymentId" not in data):
        message["response"] = "Request does not contain a deployment id."
        message["error"] = True
        return message
    
    response = reader.getTraces(
        systemId= message["data"]["systemId"],
        systemVersion= message["data"]["systemVersion"],
        deploymentId= message["data"]["deploymentId"],
    )

    if (response is None):
        message["error"] = True
        message["response"] = "An error occured while getting traces."
    else:
        message["error"] = False
        message["response"] = response

    return message


def handleUnknownCode(message):
    '''
        Handle an unkown code.
    '''
    message["response"] = f"Unknown message type: {message['code']}"
    message["error"] = True
    return message
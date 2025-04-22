import json

def handleUnknownMessage(websocket, message):
    '''
        Handle an unknown message.
    '''
    message["response"] = "Message does not contain a code"
    message["error"] = True
    return message

def handleGetSystems(reader, message):
    '''
        Get all systems.
    '''
    message["response"] = reader.getSystems()
    message["error"] = False
    return message

def handleGetPrograms(reader, message):
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

    message["response"] = reader.getPrograms(
        systemId= message["data"]["systemId"],
        systemVersion= message["data"]["systemVersion"]
    )
    message["error"] = False
    return message


def handleGetDeployments(reader, message):
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

    message["response"] = reader.getDeployments(
        systemId= message["data"]["systemId"],
        systemVersion= message["data"]["systemVersion"]
    )
    message["error"] = False
    return message


def handleGetTraces(reader, message):
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
    
    message["response"] = reader.getTraces(
        systemId= message["data"]["systemId"],
        systemVersion= message["data"]["systemVersion"],
        deploymentId= message["data"]["deploymentId"],
    )
    message["error"] = False
    return message


def handleUnknownCode(reader, message):
    '''
        Handle an unkown code.
    '''
    message["response"] = f"Unknown message type: {message['code']}"
    message["error"] = True
    return message
import json

def handleUnknownMessage(websocket, message):
    message["response"] = "Message does not contain a code"
    message["error"] = True
    return message

def handleGetSystems(reader, message):
    message["response"] = reader.getSystems()
    message["error"] = False
    return message

def handleGetPrograms(reader, websocket, message):
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


def handleGetDeployments(reader, websocket, message):
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
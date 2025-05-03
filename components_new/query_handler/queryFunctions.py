import json
from SystemDbReader import SystemDbReader

reader = SystemDbReader()

def handleUnknownMessage(message):
    '''
        Handle an unknown message.
    '''
    message["response"] = "Query did not contain a queryType key."
    message["error"] = True
    return message

def handleGetSystems(message):
    '''
        Get all systems.
    '''
    try:
        systems = reader.getSystems()
        for system in systems:
            system["deployments"] = reader.getDeployments(
                systemId= system["system_id"],
                systemVersion= system["system_ver"]
            )
        message["response"] = systems
    except Exception as e:
        message["error"] = True
        message["response"] = f"Database error: {e}"

    return message

def handleGetTraces(message):
    '''
        Get all traces given a system id, version and deployment id.
    '''
    if ("data" not in message):
        message["response"] = "Query does not contain the required data key."
        message["error"] = True
        return message
    
    data = message["data"]

    # TODO: Add missing key response to a list and return all of them.
    if ("systemId" not in data):
        message["response"] = "Query does not contain a system id."
        message["error"] = True
        return message

    if ("systemVersion" not in data):
        message["response"] = "Query does not contain a system version."
        message["error"] = True
        return message

    if ("deploymentId" not in data):
        message["response"] = "Query does not contain a deployment id."
        message["error"] = True
        return message
    
    try:    
        message["response"] = reader.getTraces(
            systemId= message["data"]["systemId"],
            systemVersion= message["data"]["systemVersion"],
            deploymentId= message["data"]["deploymentId"],
        )
    except Exception as e:
        message["error"] = True
        message["response"] = f"Database error: {e}"

    return message


def handleUnknownQueryType(message):
    '''
        Handle an unkown query type.
    '''
    message["response"] = f"Unknown message type: {message['queryType']}"
    message["error"] = True
    return message
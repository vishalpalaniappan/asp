import json
from MSG_TYPES import MSG_TYPES
from queryFunctions import *


def getMessageFromCode(code):
    '''
        Get the code description from the code.
    '''
    for key in MSG_TYPES:
        value = MSG_TYPES[key]
        if (value == code):
            return key        
    return "Unkown message code."

async def handle_query(websocket):
    '''
        Handles messages from websocket and echos a response.
    '''
    async for message in websocket:
        message = json.loads(message)        

        print(f"Received message: {getMessageFromCode(message['code'])}")
        
        if "code" not in message:
            response = handleUnknownMessage(message= message)
        
        elif (message["code"] == MSG_TYPES["GET_SYSTEMS"]):            
            response = handleGetSystems(message= message)
            
        elif (message["code"] == MSG_TYPES["GET_PROGRAMS"]):            
            response = handleGetPrograms(message= message)
        
        elif (message["code"] == MSG_TYPES["GET_DEPLOYMENTS"]):
            response = handleGetDeployments(message= message)
        
        elif (message["code"] == MSG_TYPES["GET_TRACES"]):
            response = handleGetTraces(message= message)
        
        else:
            response = handleUnknownCode(message= message)
            
        await websocket.send(json.dumps(response))

        

        

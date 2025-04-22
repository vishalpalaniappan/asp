import json
from MSG_TYPES import MSG_TYPES
from SystemDatabaseReader import SystemDatabaseReader
from queryFunctions import *

reader = SystemDatabaseReader()

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
            handleUnknownMessage(
                websocket= websocket,
                message= message
            )
        
        elif (message["code"] == MSG_TYPES["GET_SYSTEMS"]):            
            message = handleGetSystems(
                reader= reader,
                message= message
            )
            await websocket.send(json.dumps(message))
            
        elif (message["code"] == MSG_TYPES["GET_PROGRAMS"]):            
            message = handleGetPrograms(
                reader= reader,
                message= message
            )
            await websocket.send(json.dumps(message))
        
        elif (message["code"] == MSG_TYPES["GET_DEPLOYMENTS"]):
            message = handleGetDeployments(
                reader= reader,
                message= message
            )
            await websocket.send(json.dumps(message))
        
        elif (message["code"] == MSG_TYPES["GET_TRACES"]):
            message["error"] = False
            await websocket.send(json.dumps(message))
        
        else:
            message = handleUnknownCode(
                reader= reader,
                message= message
            )
            await websocket.send(json.dumps(message))

        

        

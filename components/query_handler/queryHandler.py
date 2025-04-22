import json
from MSG_TYPES import MSG_TYPES
from helper import getMessageFromCode
from queryFunctions import *

def handleQuery (message):
    '''
        Handle the query.
    '''
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

    return response

async def receieveMessage(websocket):
    '''
        Handles messages from websocket and echos a response.
    '''
    async for message in websocket:
        try:
            message = json.loads(message)   
            response = handleQuery(message=message)   
            await websocket.send(json.dumps(response))  
        except json.JSONDecodeError as e:
            response = {} 
            response["response"] = "The query does not contain a valid JSON string."
            response["error"] = False
            await websocket.send(json.dumps(response))
        

        

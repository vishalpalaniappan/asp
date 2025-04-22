import json
from MSG_TYPES import MSG_TYPES
from SystemDatabaseReader import SystemDatabaseReader
from queryFunctions import *

reader = SystemDatabaseReader()

async def handle_query(websocket):
    '''
        Handles messages from websocket and echos a response.
    '''
    async for message in websocket:
        print(f"Received message: {message}")

        message = json.loads(message)        
        
        if "code" not in message:
            handleGetSystems(
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
                websocket= websocket,
                message= message
            )
            await websocket.send(json.dumps(message))
        
        elif (message["code"] == MSG_TYPES["GET_DEPLOYMENTS"]):
            message = handleGetDeployments(
                reader= reader,
                websocket= websocket,
                message= message
            )
            await websocket.send(json.dumps(message))
        
        elif (message["code"] == MSG_TYPES["GET_TRACES"]):
            message["error"] = False
            await websocket.send(json.dumps(message))

        
        else:
            message["response"] = f"Unknown message type: {message['code']}"
            message["error"] = True
            await websocket.send(json.dumps(message))

        

        

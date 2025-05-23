import json
from queryFunctions import (
    handleUnknownMessage,
    handleGetSystems,
    handleGetTraces,
    handleUnknownQueryType
)

def handleQuery (message):
    '''
        Handle the query.
    '''
    if "queryType" not in message:
        response = handleUnknownMessage(message= message)
        return response

    print(f"Received message: {message['queryType']}")    
    
    if (message["queryType"] == "GET_SYSTEMS"):            
        response = handleGetSystems(message= message)
    
    elif (message["queryType"] == "GET_TRACES"):
        response = handleGetTraces(message= message)
    
    else:
        response = handleUnknownQueryType(message= message)

    return response

async def receiveMessage(websocket):
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
            response["error"] = True
            await websocket.send(json.dumps(response))
        

        

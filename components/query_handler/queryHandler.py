import json
from MSG_TYPES import MSG_TYPES
from SystemDatabaseReader import SystemDatabaseReader

reader = SystemDatabaseReader()

async def handle_query(websocket):
    '''
        Handles messages from websocket and echos a response.
    '''

    async for message in websocket:
        print(f"Received message: {message}")

        message = json.loads(message)
        
        # Message does not contain a valid code.
        if "code" not in message:
            message["response"] = "Message does not contain a code"
            message["error"] = True
            await websocket.send(json.dumps(message))

        # Get the systems from the database
        elif (message["code"] == MSG_TYPES["GET_SYSTEMS"]):            
            message["response"] = reader.getSystems()
            message["error"] = False
            await websocket.send(json.dumps(message))

        # Get the programs from the database
        elif (message["code"] == MSG_TYPES["GET_PROGRAMS"]):
            data = message["data"]

            if ("systemId" not in data):
                message["response"] = "Request does not contain a system id."
                message["error"] = True
                await websocket.send(json.dumps(message))            

            if ("systemVersion" not in data):
                message["response"] = "Request does not contain a system version."
                message["error"] = True
                await websocket.send(json.dumps(message))            

            message["response"] = reader.getPrograms(
                systemId= message["data"]["systemId"],
                systemVersion= message["data"]["systemVersion"]
            )
            message["error"] = False
            await websocket.send(json.dumps(message))            

        # Get the deployments from the database
        elif (message["code"] == MSG_TYPES["GET_DEPLOYMENTS"]):
            data = message["data"]

            if ("systemId" not in data):
                message["response"] = "Request does not contain a system id."
                message["error"] = True
                await websocket.send(json.dumps(message))            

            if ("systemVersion" not in data):
                message["response"] = "Request does not contain a system version."
                message["error"] = True
                await websocket.send(json.dumps(message))   

            message["response"] = reader.getDeployments(
                systemId= message["data"]["systemId"],
                systemVersion=message["data"]["systemVersion"]
            )
            message["error"] = False
            await websocket.send(json.dumps(message))

        # Get the traces from the database
        elif (message["code"] == MSG_TYPES["GET_TRACES"]):
            message["error"] = False
            await websocket.send(json.dumps(message))

        # Unknown message
        else:
            message["response"] = f"Unknown message type: {message['code']}"
            message["error"] = True
            await websocket.send(json.dumps(message))

        

        

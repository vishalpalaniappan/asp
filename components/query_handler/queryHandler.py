import json
from MSG_TYPES import MSG_TYPES

async def handle_query(websocket):
    '''
        Handles messages from websocket and echos a response.
    '''
    global processor

    async for message in websocket:
        print(f"Received message: {message}")

        message = json.loads(message)

        if "code" not in message:
            message["response"] = "Message does not contain a code"
            message["error"] = True
            await websocket.send(json.dumps(message))

        elif (message["code"] == MSG_TYPES["GET_UNIQUE_TRACES"]):
            message["error"] = False
            await websocket.send(json.dumps(message))

        elif (message["code"] == MSG_TYPES["GET_FILE_TREES"]):
            message["error"] = False
            await websocket.send(json.dumps(message))

        else:
            message["response"] = f"Unknown message type: {message['code']}"
            message["error"] = True
            await websocket.send(json.dumps(message))

        

        

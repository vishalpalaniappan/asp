from application.system_processor.SystemProcessor import SystemProcessor
import json
from application.MSG_TYPES import MSG_TYPES

SYSTEM_LOG_FILES = "./application/sample_system_logs/"
processor = SystemProcessor(SYSTEM_LOG_FILES)

async def handle_query(websocket):
    '''
        Handles messages from websocket and echos a response.
    '''
    global processor

    async for message in websocket:
        print(f"Received message: {message}")

        message = json.loads(message)

        if (message["code"] == MSG_TYPES["GET_UNIQUE_TRACES"]):
            message["response"] = processor.uniqueTraces
            message["error"] = False
        else:
            message["response"] = f"Unknown message type: {message['code']}"
            message["error"] = True

        
        await websocket.send(json.dumps(message))
        

        

from application.system_processor.SystemProcessor import SystemProcessor
    
SYSTEM_LOG_FILES = "./application/sample_system_logs/"
processor = SystemProcessor(SYSTEM_LOG_FILES)

async def handle_query(websocket):
    '''
        Handles messages from websocket and echos a response.
    '''
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(message)

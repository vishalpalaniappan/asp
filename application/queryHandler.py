async def handle_query(websocket):
    '''
        Handles messages from websocket and echos a response.
    '''
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send(message)

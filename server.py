#!/usr/bin/env python

import asyncio
from websockets.asyncio.server import serve
from application.queryHandler import handle_query

async def main():
    '''
        Creates a websocket at the provided port and initializes
        the query handler.
    '''
    async with serve(handle_query, "localhost", 8765) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())
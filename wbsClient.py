import asyncio
import websockets


async def receiveData():
    async with websockets.connect('ws://localhost:5000') as websocket:
        data = await websocket.recv()
        print(data)
while True:
    asyncio.get_event_loop().run_until_complete(receiveData())


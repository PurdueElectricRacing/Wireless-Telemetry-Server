import asyncio
import websockets

ip = "localhost"
port = 5000
data = []
async def getData():
    """CODE THAT GETS CAN DATA """

async def sendData(websocketIp):
    await websocketIp.send(str(data))

async def main(ip, port):
    """getData and sendData are ran concurrently to allow simultaneously updating and data transmission"""
    sendData_Task = asyncio.create_task(sendData(ip))
    getData_Task = asyncio.create_task(getData())
    await sendData_Task
    await getData_Task


server = websockets.serve(main, ip, port)
print("Server established at ws://{}:{}".format(ip, port))
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
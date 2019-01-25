import WirelessTelemServer as server
import asyncio
import random

# This file simulates the job of the DAQ code.
# A server is setup and broadcast on ip:port
# Data is sent every second to simulate reading the CAN bus

ip = '127.0.0.1'
port = 5000


async def send_data():
    while True:
        await asyncio.sleep(1)
        data = {
                "accel": random.random() * 10,
                "gyro": random.random() * 360,
                "angle": random.random() * 180
                }
        await server.send_data(data)


async def run_server(ip, port):
    wait_task = asyncio.ensure_future(send_data())
    server_task = asyncio.ensure_future(server.get_server('127.0.0.1', 5000))
    print(f'Serving websocket server on {ip}:{port} ...')

    done, pending = await asyncio.wait(
        [wait_task, server_task],
        return_when=asyncio.ALL_COMPLETED
    )

asyncio.get_event_loop().run_until_complete(run_server(ip, port))

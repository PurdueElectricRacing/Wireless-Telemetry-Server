import WirelessTelemServer as server
import asyncio
import random
import time

# This file simulates the job of the DAQ code.
# A server is setup and broadcast on ip:port
# Data is sent every second to simulate reading the CAN bus

ip = '127.0.0.1'
port = 5000

possible_data = [
    {
        'i': '501',
        'm': '0F900EBF02A0029F',
        'ts': None
    },
]


async def send_data():
    while True:
        await asyncio.sleep(0.01)
        index = int(random.random() * len(possible_data))
        data = possible_data[index]
        data['ts'] = int(time.time()*1000)
        await server.send_data([data])


async def run_server(ip, port):
    wait_task = asyncio.ensure_future(send_data())
    server_task = asyncio.ensure_future(server.get_server(ip, port))

    done, pending = await asyncio.wait(
        [wait_task, server_task],
        return_when=asyncio.ALL_COMPLETED
    )

asyncio.get_event_loop().run_until_complete(run_server(ip, port))

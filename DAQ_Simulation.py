import WirelessTelemServer as server
import asyncio
import random

# This file simulates the job of the DAQ code.
# A server is setup and broadcast on ip:port
# Data is sent every second to simulate reading the CAN bus

ip = '127.0.0.1'
port = 5000


possible_data = [
    # {
    #     'id': '421',
    #     'data': '03FFBA00776F'
    # },
    # {
    #     'id': '422',
    #     'data': '68090000'
    # },
    # {
    #     'id': '421',
    #     'data': '01FFC000777F'
    # },
    # {
    #     'id': '421',
    #     'data': '00FFF70077FF'
    # },
    # {
    #     'id': '601',
    #     'data': '00010000'
    # },
    # {
    #     'id': '6B0',
    #     'data': '00010B90C710416C'
    # },
    {
        'id': '501',
        'data': '0F900EBF02A0029F'
    },
]


async def send_data():
    while True:
        await asyncio.sleep(0.01)
        index = int(random.random() * len(possible_data))
        data = possible_data[index]
        await server.send_data(data)


async def run_server(ip, port):
    wait_task = asyncio.ensure_future(send_data())
    server_task = asyncio.ensure_future(server.get_server('127.0.0.1', 5000))

    done, pending = await asyncio.wait(
        [wait_task, server_task],
        return_when=asyncio.ALL_COMPLETED
    )

asyncio.get_event_loop().run_until_complete(run_server(ip, port))

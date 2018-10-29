import WirelessTelemServer as server
import asyncio
import random
import serial_asyncio
import time
import datetime

# This will run on startup on the RPI.

# Using different threads, this file will setup a
# websocket server @ 192.168.4.1:5000 and broadcast
# every CAN message from the car.

ip = '192.168.4.1'
port = 5000


# Used to setup and open CANdapter, only runs once.
async def write_serial_data(serial_connection):
    serial_connection.write(b'A1\r')    # Enable Timestamps
    serial_connection.write(b'S6\r')    # CAN Baudrate set to 500k
    serial_connection.write(b'O\r')     # Open CANdapter


# Read serial data from the CANdapter
async def rec_serial_data(serial_connection):
    while True:
        # Message EOF is a \r character
        message_raw = await serial_connection.readuntil(b'\r')

        # Message format
        # tIIILDDDDDDDD
        # III = CAN ID
        # L = Message Length
        # D = Message data

        # Remove trailing \r and leadting t character
        message = message_raw.replace(b'\r', b'')[1:].decode("utf-8", "ignore")

        m_id = message[0:3]
        m_len = message[3:4]
        m_message = message[4:-4]
        m_time_stamp = str(datetime.datetime.now())

        data = {
            "id": m_id,
            "length": m_len,
            "message": m_message,
            "timestamp": m_time_stamp
            }

        await server.send_data(data)


async def main(loop):
    reader, writer = await serial_asyncio.open_serial_connection(
        url='/dev/ttyUSB0', baudrate=2500000)

    read_task = asyncio.ensure_future(rec_serial_data(reader))
    write_task = asyncio.ensure_future(write_serial_data(writer))

    server_task = asyncio.ensure_future(server.get_server(ip, port))

    done, pending = await asyncio.wait(
        [read_task, write_task, server_task],
        return_when=asyncio.ALL_COMPLETED
    )

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

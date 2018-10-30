import WirelessTelemServer as server
import asyncio
import random
import serial_asyncio
import time
from datetime import datetime
import logging
import os.path

# This will run on startup on the RPI.

# Using different threads, this file will setup a
# websocket server @ 192.168.4.1:5000 and broadcast
# every CAN message from the car.

ip = '192.168.4.1'
port = 5000

start_date_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

start_path = os.path.abspath(os.path.dirname(__file__))
log_path = os.path.join(start_path, 'logs',
                        start_date_time + '.txt')
# configure logger to not format messages
logging.basicConfig(level=logging.DEBUG, filename=log_path,
                    filemode="a+", format='%(message)s')

data_logger = logging.getLogger(__name__)
logging.getLogger("asyncio").setLevel(logging.WARNING)

data_logger.info(start_date_time)

# Max resolution (ms) for data frames to be logged
max_time_diff_ms = 100
start_time = int(round(time.time() * 1000))
last_time = start_time
multi_frame_message = ''


# Logs a set of CAN frames in a time interval to a log file
async def log_CAN_data(timestamp, can_id, length, message):
    current_time = int(round(time.time() * 1000))

    # Wait for serial connection to stabalize, avoid garbage data
    if current_time - start_time < 1500:
        return

    global last_time, multi_frame_message

    delta_time = current_time - last_time
    single_frame = ',' + can_id + ',' + length + ',' + message

    if(delta_time >= max_time_diff_ms):
        data_logger.info(multi_frame_message)
        last_time = current_time
        multi_frame_message = str(current_time - start_time) + single_frame
    else:
        multi_frame_message += single_frame


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
        m_timestamp = str(datetime.now())

        await log_CAN_data(m_timestamp, m_id, m_len, m_message)

        data = {
            "id": m_id,
            "length": m_len,
            "message": m_message,
            "timestamp": m_timestamp
            }

        await server.send_data(data)


async def main(loop):
    serial_reader, serial_writer = await serial_asyncio.open_serial_connection(
        url='/dev/ttyUSB0', baudrate=2500000)

    read_task = asyncio.ensure_future(rec_serial_data(serial_reader))
    write_task = asyncio.ensure_future(write_serial_data(serial_writer))

    server_task = asyncio.ensure_future(server.get_server(ip, port))

    done, pending = await asyncio.wait(
        [read_task, write_task, server_task],
        return_when=asyncio.ALL_COMPLETED
    )

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

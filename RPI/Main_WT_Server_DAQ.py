import WirelessTelemServer as server
import asyncio
import serial_asyncio
import time
from datetime import datetime
import os.path
import CAN_Logger

# This will run on startup on the RPI.

# Using different threads, this file will setup a
# websocket server @ 192.168.10.1:5000 and broadcast
# every CAN message from the car.
# Information is available on the wiki page here:
# http://purdueelectricracing.com/wiki/index.php/Wireless_Telemetry
ip = '192.168.10.1'
port = 5000

start_date_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

start_path = os.path.abspath(os.path.dirname(__file__))
log_path = os.path.join(start_path, 'logs',
                        start_date_time + '.txt')

with open(log_path, 'a+') as logfile:
    logfile.write(start_date_time)

# Max resolution (ms) for data frames to be logged
max_time_diff_ms = 100  # Rate of 10Hz
start_time = int(round(time.time() * 1000))
last_time = start_time
multi_frame_message = ''


# Used to setup and open CANdapter, only runs once.
async def write_serial_data(serial_connection):
    serial_connection.write(b'A1\r')    # Enable Timestamps
    serial_connection.write(b'S6\r')    # CAN Baudrate set to 500k
    serial_connection.write(b'O\r')     # Open CANdapter


# Read serial data from the CANdapter
async def rec_serial_data(serial_connection):
    current_time = time.time()
    last_time = current_time
    # buffer_time = 1/500
    buffer_time = 0

    buffer = {}
    while True:
        # Message EOF is a \r character
        message_raw = await serial_connection.readuntil(b'\r')

        # Message format
        # tIIILDDDDDDDD
        # III = CAN ID
        # L = Message Length
        # D = Message data

        # Remove trailing \r and leadting t character
        can_message = message_raw.replace(b'\r', b'')[1:].decode("utf-8", "ignore")

        m_id = can_message[0:3]  
        stripped_message = can_message[3:]

        num_id = None
        m_timestamp = int(round(time.time() * 1000))

        CAN_Logger.log_CAN_data(m_id, m_timestamp)

        try:
            num_id = int(m_id, 16)
        except Exception:
            continue

        log_CAN_data(m_id, stripped_message)

        data = {
            "i": m_id,
            "m": stripped_message,
            "ts": m_timestamp
            }
        buffer[int(m_id, 16)] = data

        current_time = time.time()
        if current_time - last_time >= buffer_time:
            buffer_len = len(buffer)
            if buffer_len > 0:
                last_time = current_time
                await server.send_data(buffer)
                buffer = {}


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

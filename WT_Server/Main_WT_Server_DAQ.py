import WirelessTelemServer as server
import asyncio
import serial_asyncio
import serial
import time
from datetime import datetime
import os.path
import CAN_Logger
import sys

# This will run on startup on the RPI.

# Using different threads, this file will setup a
# websocket server @ 192.168.10.1:5000 and broadcast
# every CAN message from the car.
# Information is available on the wiki page here:
# http://purdueelectricracing.com/wiki/index.php/Wireless_Telemetry

ip = '192.168.10.1'
port = 5000
SER_PORT = '/dev/ttyUSB0'
SER_RATE = 5000000
ENABLE_WEBSOCKETS = False

if(len(sys.argv)) > 1:
    ip = sys.argv[1]

start_date_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

start_path = os.path.abspath(os.path.dirname(__file__))
log_path = os.path.join(start_path, 'logs',
                        start_date_time + '.txt')

with open(log_path, 'a+') as logfile:
    logfile.write(start_date_time)

# Max resolution (ms) for data frames to be logged
start_time = int(round(time.time() * 1000))
last_time = start_time
multi_frame_message = ''


def close_CANDAPTER(serial_connection):
    close_message = "\rC\r".encode()
    print(serial_connection.write(close_message))
    serial_connection.flush()
    serial_connection.reset_output_buffer()
    serial_connection.close()
    print("Done cleaning CANDapter...")


def initalize_CANDAPTER(serial_connection):
    baudrate = 'S6\r'.encode()          # CAN Baudrate set to 500k
    timestamp = 'A0\r'.encode()         # Enable timestamps
    open_message = 'O\r'.encode()       # Open connection to CANDAPTER
    clear_message = '\r\r\r'.encode()

    serial_connection.write(baudrate)
    serial_connection.write(timestamp)
    serial_connection.write(clear_message)
    serial_connection.write(open_message)

    print("Done init CANDapter...")


# Read serial data from the CANdapter
async def rec_serial_data(ser_read, ser_write):
    current_time = time.time()
    last_time = current_time
    buffer_time = 1/100
    # buffer_time = 0

    parsed_buffer = {}
    message_buffer = bytes()

    initalize_CANDAPTER(ser_write)
    time.sleep(1)

    while True:

        # EXPERIMENTAL
        # if not server.can_to_send == "":
        #     print("Message to send over CAN: " + server.can_to_send.encode)
        #     ser_write.write(server.can_to_send.encode() + b"\r")
        #     server.can_to_send = ""
        #     await ser_write.drain()

        in_byte = await ser_read.read(1)
        print(in_byte)

        if b"\x06" in in_byte:
            # CANDapter has recieved our command.
            print("CANDapter acknowledged command.")
        elif b"\x07" in in_byte:
            # CANDapter error
            print("CANDApter Error")
        elif b"\r" in in_byte:
            # End of CAN frame
            raw_message = message_buffer.decode().strip().replace("\r", "")

            if "t" not in raw_message:
                # Reset message buffer if invalid message was recieved
                message_buffer = bytes()
                continue

            # Strip initial 't' off of the message
            t_index = raw_message.index("t")
            can_message = raw_message[t_index + 1:]

            m_id = can_message[0:3]
            stripped_message = can_message[3:]

            num_id = None
            m_timestamp = int(round(time.time() * 1000))

            try:
                num_id = int(m_id, 16)
            except Exception:
                continue

            data = {
                "i": m_id,
                "m": stripped_message,
                "ts": m_timestamp
                }
            parsed_buffer[int(m_id, 16)] = data

            # Log all data to the logfile. Can be done periodically
            # by placing this line in the below FOR loop.
            # ENABLE_WEBSOCKETS must be enabled to do so.
            CAN_Logger.log_CAN_data(num_id, data)

            current_time = time.time()
            if ENABLE_WEBSOCKETS and current_time - last_time >= buffer_time:
                buffer_len = len(parsed_buffer)
                if buffer_len > 0:
                    last_time = current_time
                    await server.send_data(parsed_buffer)
                    parsed_buffer = {}

            # Clear message buffer once we are done with it.
            message_buffer = bytes()

        else:
            # Part of CAN frame, append to message being recieved
            message_buffer += in_byte


async def main(loop):
    serial_reader, serial_writer = await serial_asyncio.open_serial_connection(
        url=SER_PORT, baudrate=SER_RATE
        )

    ser_task = asyncio.ensure_future(
        rec_serial_data(serial_reader, serial_writer)
        )

    server_task = asyncio.ensure_future(
        server.get_server(ip, port)
        )

    done, pending = await asyncio.wait(
        [ser_task, server_task],
        return_when=asyncio.ALL_COMPLETED
        )


ser = serial.Serial(SER_PORT, SER_RATE)
# Close candapter at start to avoid any loose messages in the queue.
close_CANDAPTER(ser)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

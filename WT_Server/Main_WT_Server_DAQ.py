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

ID_FILTER = [
    '0A0', # MC Temp 1
    '0A1', # MC Temp 2
    '0A2', # MC Temp 3
    '0A6', # MC Current
    '0A7', # MC Voltage
    '0A8', # MC Flux
    '0AC', # MC Torque
    '700', # Wheel Speed
    '701', # Wheel Speed
    '421', # Accel
    '720', # Coolant 
    '721', # Coolant Flow
    '6B1' # SOC Data
]

if(len(sys.argv)) > 1:
    ip = sys.argv[1]

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

    parsed_buffer = {}
    message_buffer = bytes()

    initalize_CANDAPTER(ser_write)
    time.sleep(1)

    START_LOGGING = True

    while True:

        # EXPERIMENTAL
        # if not server.can_to_send == "":
        #     print("Message to send over CAN: " + server.can_to_send.encode)
        #     ser_write.write(server.can_to_send.encode() + b"\r")
        #     server.can_to_send = ""
        #     await ser_write.drain()

        in_byte = await ser_read.read(1)
        if b"\x06" in in_byte:
            # CANDapter has recieved our command.
            print("CANDapter acknowledged command.")
        elif b"\x07" in in_byte:
            # CANDapter error
            print("CANDApter Error")
        elif b"\r" in in_byte:
            # End of CAN frame
            raw_message = message_buffer.decode().strip().replace("\r", "")
            message_buffer = bytes()
            if "t" not in raw_message:
                # Reset message buffer if invalid message was recieved
                continue
            
            # Strip initial 't' off of the message
            t_index = raw_message.index("t")

            can_message = raw_message[t_index + 1:]

            m_id = can_message[0:3]
            if not START_LOGGING:
                if '350' in m_id:
                    START_LOGGING = True
                    print("Start button pressed! Logging data...\n")
                    CAN_Logger.create_logfile()
            else:
                if m_id in ID_FILTER:
                    stripped_message = can_message[4:]
                    CAN_Logger.log_CAN_data(m_id, stripped_message)
            
            


            # m_timestamp = int(round(time.time() * 1000))

            # data = {
            #     "i": m_id,
            #     "m": stripped_message,
            #     "ts": m_timestamp
            #     }
            # parsed_buffer[num_id] = data

            # Log all data to the logfile. Can be done periodically
            # by placing this line in the below FOR loop.
            # ENABLE_WEBSOCKETS must be enabled to do so.
            

            # current_time = time.time()
            # if ENABLE_WEBSOCKETS and current_time - last_time >= buffer_time:
            #     buffer_len = len(parsed_buffer)
            #     if buffer_len > 0:
            #         last_time = current_time
            #         await server.send_data(parsed_buffer)
            #         parsed_buffer = {}

            # Clear message buffer once we are done with it.
            

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

    if ENABLE_WEBSOCKETS:
        server_task = asyncio.ensure_future(
            server.get_server(ip, port)
            )
        done, pending = await asyncio.wait(
            [ser_task, server_task],
            return_when=asyncio.ALL_COMPLETED
            )
    else:
        done, pending = await asyncio.wait(
            [ser_task],
            return_when=asyncio.ALL_COMPLETED
            )


ser = serial.Serial(SER_PORT, SER_RATE)
# Close candapter at start to avoid any loose messages in the queue.
close_CANDAPTER(ser)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))

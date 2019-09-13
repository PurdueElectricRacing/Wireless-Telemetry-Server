import serial
import time
from datetime import datetime
import CAN_Logger
import sys

# This will run on startup on the RPI.

# Using different threads, this file will setup a
# websocket server @ 192.168.10.1:5000 and broadcast
# every CAN message from the car.
# Information is available on the wiki page here:
# http://purdueelectricracing.com/wiki/index.php/Wireless_Telemetry

SER_PORT = '/dev/ttyUSB0'
SER_RATE = 500000

ID_FILTER = [
    '0A0', # MC Temp 1 10100000
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


def close_CANDAPTER(serial_connection):
    close_message = "\rC\r".encode()
    print(serial_connection.write(close_message))
    serial_connection.flush()
    serial_connection.reset_output_buffer()
    serial_connection.close()
    print("[INFO] Done cleaning CANDapter...")


def initalize_CANDAPTER(serial_connection):
    baudrate = 'S6\r'.encode()          # CAN Baudrate set to 500k
    timestamp = 'A0\r'.encode()         # Enable timestamps
    open_message = 'O\r'.encode()       # Open connection to CANDAPTER
    clear_message = '\r\r\r'.encode()

    serial_connection.write(baudrate)
    serial_connection.write(timestamp)
    serial_connection.write(clear_message)
    serial_connection.write(open_message)

    print("[INFO] Done init CANDapter...")


# Read serial data from the CANdapter
def start_data_collection(ser_port):
    message_buffer = bytes()

    initalize_CANDAPTER(ser_port)
    time.sleep(1)

    START_LOGGING = False
    print("[INFO] Begin CAN bus listening...")

    while True:
        # Read all data waiting in the buffer
        message_buffer += ser_port.read()


        # Messages are deliniaed with a \r char. The last message might not be complete so it
        # must be carrried over to the next iteration
        finished_messages = message_buffer.split("\r")
        message_buffer = finished_messages[-1]

        # Do not iterate over the last message in the buffer, it might be incomplete.
        num_messages = len(finished_messages) - 1
        for message_index in range(num_messages):
            raw_message = finished_messages[message_index]

            # clean messsage from serial read
            clean_message = raw_message.decode().strip().replace("\r", "")

            # All valid can messages begin with a 't' character
            if not clean_message.startswith('t'):
                # Reset message buffer if invalid message was recieved
                print(f"[WARN] Invalid message recieved: {clean_message}")
                continue
            
            # Strip initial 't' off of the message
            can_message = clean_message[1:]

            if not len(can_message) > 4:
                print(f"[WARN] Invalid message recieved: {clean_message}")
                continue

            m_id = can_message[0:3]
            if not START_LOGGING:
                if '350' in m_id:
                    START_LOGGING = True
                    print("[INFO] Start button pressed! Begin logging data...\n")
                    CAN_Logger.create_logfile()
            else:
                if m_id in ID_FILTER:
                    stripped_message = can_message[4:]
                    CAN_Logger.log_CAN_data(m_id, stripped_message)


# Close candapter at start to avoid any loose messages in the queue.
close_CANDAPTER(serial.Serial(SER_PORT, SER_RATE))

start_data_collection(serial.Serial(SER_PORT, SER_RATE))


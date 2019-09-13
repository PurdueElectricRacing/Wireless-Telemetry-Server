import asyncio
import serial_asyncio
import serial
import time
from datetime import datetime
import os.path
import sys

def close_CANDAPTER(serial_connection):
    close_message = "\rC\r".encode()
    # print(serial_connection.write(clear_message))   # CAN Baudrate set to 500k
    print(serial_connection.write(close_message))   # CAN Baudrate set to 500k
    serial_connection.flush()
    serial_connection.reset_output_buffer()
    serial_connection.close()
    print("Done cleaning CANDapter...")

def initalize_CANDAPTER(serial_connection):
    baudrate = 'S7\r'.encode()
    timestamp = 'A0\r'.encode()
    open_message = 'O\r'.encode()
    ver_message = 'V\r'.encode()
    close_message = "\rC\r".encode()
    clear_message = '\r\r\r'.encode()
    # serial_connection.write(ver_message)

    serial_connection.write(baudrate)   # CAN Baudrate set to 500k
    serial_connection.write(timestamp)   # CAN Baudrate set to 500k
    serial_connection.write(clear_message)   # CAN Baudrate set to 500k
    serial_connection.write(open_message)   # CAN Baudrate set to 500k

    print("Done init CANDapter...")


# Used to setup and open CANdapter, only runs once.
# async def write_serial_data(ser):
#     print("Write task")
#     while True:
#         print("Sending..")
#         await ser.write(b"T3CF411223344\r")

async def rec_serial_data(ser_read, ser_write):
    current_time = time.time()
    print("[Rec Serial Data Task] Start")
    last_time = current_time
    # buffer_time = 1/500
    buffer_time = 0

    parsed_buffer = {}
    message_buffer = bytes()
    initalize_CANDAPTER(ser_write)
    time.sleep(1)

    while True:
        # Message EOF is a \r character
        in_byte = await ser_read.read(1)

        if b"\x06" in in_byte:
            print("ACK")
        elif b"\x07" in in_byte:
            print("CANDApter Error")
        elif b"\r" in in_byte:

            raw_message = message_buffer.decode().strip().replace("\r", "")

            if "t" not in raw_message:
                message_buffer = ""
                continue
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
        
            current_time = time.time()
            if current_time - last_time >= buffer_time:
                buffer_len = len(parsed_buffer)
                if buffer_len > 0:
                    last_time = current_time
                    
                    parsed_buffer = {}

            message_buffer = bytes()
        else:
            message_buffer += in_byte

        if False:
            ser_write.write(b"T3CF411223344\r")
            await ser_write.drain()


async def main(loop):
    serial_reader, serial_writer = await serial_asyncio.open_serial_connection(
        url='COM29', baudrate=5000000)
    

    loop = asyncio.get_event_loop()

    # asyncio.ensure_future(reader)
    # print('Reader scheduled')

    # initalize_CANDAPTER(serial_writer)

    ser_task = asyncio.ensure_future(rec_serial_data(serial_reader, serial_writer))
    # write_task = asyncio.ensure_future(write_serial_data(serial_writer))


    done, pending = await asyncio.wait(
        [ser_task],
        return_when=asyncio.ALL_COMPLETED
    )

ser = serial.Serial('COM29', 5000000)
close_CANDAPTER(ser)

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))


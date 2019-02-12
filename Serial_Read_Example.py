import serial
import time
import datetime

ser = serial.Serial('/dev/ttyUSB0', 2500000, timeout=None)

print(ser.write('S6\r'))    # CAN Baudrate set to 500k
print(ser.write('O\r'))     # Open CANdapter

while True:
    in_wait = ser.in_waiting
    if(in_wait > 0):
        try:
            # Message format
            # tIIILDDDDDDDDTTTT
            # III = CAN ID
            # L = Message Length
            # D = Message data
            # T = Timestamp

            message = ser.read_until('\r').replace('\r', '')[1:]

            m_id = message[0:3]
            m_len = message[3:4]
            m_message = message[4:-4]
            m_time_stamp = str(datetime.datetime.now())
            print("id: " + m_id + "\t\tlen: " + m_len +
                  "\t\ttime_stamp: " m_time_stamp + "\tmsg: " + m_message)

        except (serial.serialutil.SerialException):
            print(str(in_wait) + " !!!!")

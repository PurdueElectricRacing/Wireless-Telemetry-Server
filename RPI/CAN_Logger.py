import os.path
from datetime import datetime
import time
import sys

start_date_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

start_path = os.path.abspath(os.path.dirname(__file__))
log_path = os.path.join(start_path, 'logs',
                        start_date_time + '.txt')

with open(log_path, 'a+') as logfile:
    logfile.write(start_date_time)

# Max resolution (ms) for data frames to be logged
max_time_diff_ms = 1000  
start_time = int(round(time.time() * 1000))
last_time = start_time
multi_frame_message = ''

total_size = 0


# Logs a set of CAN frames in a time interval to a log file
def log_CAN_data(can_id, message):
    return
    current_time = int(round(time.time() * 1000))

    global start_time

    # Wait for serial connection to stabilize, avoid garbage data
    if current_time - start_time < 1500:
        return

    global last_time, multi_frame_message, log_path, total_size

    delta_time = current_time - last_time
    single_frame = ';' + str(hex(can_id)) + ',' + str(message)

    if(delta_time >= max_time_diff_ms):
        with open(log_path, 'a+') as logfile:
            logfile.write("\n" + multi_frame_message)
        last_time = current_time

        total_size += sys.getsizeof(multi_frame_message)
        print(total_size)

        multi_frame_message = str(current_time - start_time) + single_frame
    else:
        multi_frame_message += single_frame

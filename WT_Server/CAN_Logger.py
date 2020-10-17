import os.path
from datetime import datetime
import time
import sys
import csv

log_path = ''

# Max resolution (ms) for data frames to be logged
max_time_diff_ms = 10
start_time = int(round(time.time() * 1000))
last_time = start_time
multi_frame_message = []

def log_string(message):
    global log_path
    with open(log_path, 'a+') as logfile:
        logfile.write(message)

#Same concept as SensorDict's save_data_to_csv(    
def log_csv(input_list):
    global log_path
    with open(log_path, 'a+') as fid:
            logfile = csv.DictWriter(fid, 
                                    fieldnames=["timestamp", "id", "data"],
                                    extrasaction="ignore")
            for dictionary in input_list:
                logfile.writerow(dictionary)

def create_logfile():
    print("[INFO] Creating logfile...")
    global log_path

    start_date_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    start_path = os.path.abspath(os.path.dirname(__file__))

    log_path = os.path.join(start_path, 'logs',
                        start_date_time + '.csv')

    #log_string(start_date_time)
    log_csv([{"id": "id", "data": "data", "timestamp": "timestamp"}])

    print("[INFO] Logfile created: {}.csv".format(start_date_time))
    

# Logs a set of CAN frames in a time interval to a log file
def log_CAN_data(can_id, message):

    current_time = int(round(time.time() * 1000))

    global start_time

    # Wait for serial connection to stabilize, avoid garbage data
    if current_time - start_time < 1500:
        return

    global last_time, multi_frame_message, log_path

    delta_time = current_time - last_time
    single_frame = {"id": str(can_id), "data": str(message), "timestamp": str(current_time-start_time)}

    multi_frame_message.append(single_frame)

    if(delta_time >= max_time_diff_ms):
        log_csv(multi_frame_message)
        last_time = current_time
        print(str(multi_frame_message))
        multi_frame_message.clear()


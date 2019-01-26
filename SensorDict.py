import csv

# Import sensor data from CSF file. This file contains information
# about each individual sensor on the car as well as its can ID
# and data offset used to parse the specific sensor's data

sensor_file = csv.DictReader(open("SensorDict.csv"))

# Sensor ID values are in base 16
sensors = {(int(row['id'], 16), row['name']) for row in sensor_file}

# Start by printing all data imported by the file
for s in sensors:
    print(s)

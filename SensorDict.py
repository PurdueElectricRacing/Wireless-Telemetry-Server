import csv

# Import sensor data from CSF file. This file contains information
# about each individual sensor on the car as well as its can ID
# and data offset used to parse the specific sensor's data

sensor_file = csv.DictReader(open('SensorDict.csv'))

for row in sensor_file:
    if row:
        row['id'] = int(row['id'].strip(), 16)
        row['start_byte'] = int(row['start_byte'].strip())
        row['end_byte'] = int(row['end_byte'].strip())
        row['name'] = row['name'].strip()
        print(row['comment'])

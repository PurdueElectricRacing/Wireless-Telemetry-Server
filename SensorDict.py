import csv

# Import sensor data from CSF file. This file contains information
# about each individual sensor on the car as well as its can ID
# and data offset used to parse the specific sensor's data

sensor_file = csv.DictReader(open('SensorDict.csv'))


# When run as main, output current sensor CSV data to a format
# for pasting into the Wiki
if __name__ == '__main__':
    print("{| class=\"wikitable\"")
    print("|-")
    print("!ID")
    print("!Name")
    print("![MSB:LSB]")
    print("!Comments")
    print("|-")
    for row in sensor_file:
        if row:
            row['id'] = (row['id'].strip())
            row['LSB'] = int(row['LSB'].strip())
            row['MSB'] = int(row['MSB'].strip())
            row['name'] = row['name'].strip()

            print("|", row['id'])
            print("|", row['name'])
            print("|[" + str(row['MSB']) + ":" + str(row['LSB'])+"]")
            print("|", row['comments'])
            print("|-")
    print("|}")

import csv

# Import sensor data from CSF file. This file contains information
# about each individual sensor on the car as well as its can ID
# and data offset used to parse the specific sensor's data

sensor_file = csv.DictReader(open('SensorDict.csv'))

# Takes in a dictionary file with the format for all of the sensor data
# Takes in a dictionary with format {'id': 'XXX', 'data': 'XXXXXXXX...'}
# Returns a dictionary with the data split up with corresponding names
def data_to_dict(dict_file, data):
    id = "0x" + data["id"]
    message = data["data"]
    output_dict = {}
    for row in dict_file:
        if (row["id"] != id):
            continue
        lsb = int(row["LSB"]) # Least significant byte
        msb = int(row["MSB"]) + 1 # Most significant byte + 1
        name = row["name"] # Each entry with a matching ID has a name that goes in the returned dictionary
        output_dict[name] = message[lsb:msb][::-1] # Collects from lsb to msb and then reverses it
    return output_dict


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

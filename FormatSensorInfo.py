from SensorDict import sensor_file
import sys


# When run as main, output current sensor CSV data to a format
# for pasting into the Wiki
if __name__ == '__main__':
    if len(sys.argv) >= 2:

        if sys.argv[1] == 'sheets':
            formattedIDs = {}
            for row in sensor_file:
                canID = int(row['id'], 16)
                msb = int(row['MSB'])
                lsb = int(row['LSB'])
                if row:
                    cell = ''
                    numBytes = lsb - msb + 1
                    for byte in range(numBytes):
                        startBit = (numBytes - byte) * 8 - 1
                        endBit = (numBytes - byte - 1) * 8
                        cell += ',' + row['name'] + \
                            " (" + str(startBit) + ":" + str(endBit) + ")"

                    if canID not in formattedIDs:
                        formattedIDs[canID] = row['id'] + ', '
                    formattedIDs[canID] += cell
            for line in formattedIDs:
                print(formattedIDs[line])

        elif sys.argv[1] == 'wiki':
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

import sys
from SensorDict import CANParser

parser = CANParser()


# When run as main, output current sensor CSV data to a format
# for pasting into the Wiki
if __name__ == '__main__':
    if len(sys.argv) >= 2:

        if sys.argv[1] == 'sheets':
            outputList = {}

            for canId in parser.sensorLib:
                idEntry = parser.sensorLib[canId]
                hexId = hex(canId)
                desc = idEntry.keys()[0].rsplit('_', 1)[0]

                outputText = desc + ',' + hexId + ', '

                for sensorName in idEntry:
                    sensorData = idEntry[sensorName]
                    msb = int(sensorData[0])
                    lsb = int(sensorData[1])

                    cell = ''
                    numBytes = lsb - msb + 1
                    for byte in range(numBytes):
                        startBit = (numBytes - byte) * 8 - 1
                        endBit = (numBytes - byte - 1) * 8
                        outputText += ',' + sensorName + \
                            " (" + str(startBit) + ":" + str(endBit) + ")"

                outputList[canId] = outputText

            for canID in sorted(outputList):
                print(outputList[canID])

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

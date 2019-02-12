import sys
from SensorDict import CANParser

parser = CANParser()

# Display formatted text for either pasting into google sheets
# or on the wiki for reference.
if __name__ == '__main__':
    if len(sys.argv) >= 2:

        # Output for google sheets with the following output:
        # Name, ID, , SensorName (ByteN), SensorName (ByteN-1), ...
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

        # Outputs all data in the wiki markdown format for a table
        # ID, Name, [MSB:LSB]
        elif sys.argv[1] == 'wiki':
            print("{| class=\"wikitable\"")
            print("|-")
            print("!ID")
            print("!Name")
            print("![MSB:LSB]")
            print("|-")
            for canIDDec in parser.sensorLib:
                idEntry = parser.sensorLib[canIDDec]
                canID = hex(canIDDec)

                for sensorName in idEntry:
                    sensorData = idEntry[sensorName]
                    msb = int(sensorData[0])
                    lsb = int(sensorData[1])

                    print("|", canID)
                    print("|", sensorName)
                    print("|[" + str(msb) + ":" + str(lsb)+"]")
                    print("|-")
            print("|}")

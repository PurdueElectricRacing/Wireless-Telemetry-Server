import csv


# Import sensor data from CSV file. This file contains information
# about each individual sensor on the car as well as its can ID
# and data offset used to parse the specific sensor's data
class CANParser():
    def __init__(self):
        self.sensorLib = self.create_lib()

        self.saveFile = csv.DictWriter(open('SensorData.csv', "a"),
                                       fieldnames=["timestamp", "id", "data"],
                                       extrasaction="ignore")

    # Parses CSV file of individual sensors to a dict that is easily
    # navigitable for parsing incoming data.
    # list format:
    # id : {'name1' : [msb, lsb], 'name2' : [msb, lsb], ...}
    def create_lib(self):
        sensorLibraryFile = csv.reader(open('SensorDict.csv'))
        sensorIdList = {}

        for row in sensorLibraryFile:
            if not row or row[0] == 'id':
                continue

            canID = int(row[0], 16)
            msb = int(row[1])
            lsb = int(row[2])
            friendlyName = row[3].strip()

            if canID not in sensorIdList:
                sensorIdList[canID] = {}
            sensorIdList[canID][friendlyName] = [msb, lsb]

        return sensorIdList

    # Takes in a single data point with the format:
    # {"timestamp" : "XXX", "id" : "XXX", "data" : "XXXX"}
    # This is how the websocket sends single data points
    # Returns a dictionary with the data split up with corresponding names
    # and split up datapoints.
    def parse_single_data(self, dataLine, convert=False):
        messageID = int(dataLine["id"], 16)
        message = dataLine["data"]
        timestamp = dataLine["timestamp"]

        output_dict = {}

        libFormat = self.sensorLib[messageID]

        for sensorName in libFormat:
            indicies = libFormat[sensorName]
            msb = indicies[0]
            lsb = indicies[1] + 1
            dataValue = message[msb:lsb]
            if convert:
                dataValue = int(dataValue, 16)
            output_dict[sensorName] = dataValue

        output_dict['timestamp'] = dataLine['timestamp']
        return output_dict

    # Takes in a list of dictionaries in the format:
    # {"timestamp" : "XXX", "id" : "XXX", "data" : "XXX"}
    # And saves each one in SensorData.csv (defined as sensor_data)
    # APPEND to SensorData.csv with fields timestamp,id,data
    def save_data_to_csv(input_list):
        for dictionary in input_list:
            self.saveFile.writerow(dictionary)


# Sample use code of parsing class
if __name__ == "__main__":
    sampleParser = CANParser()
    sampleWSData = [
        {"id": "760", "data": "FFCDEFAB", "timestamp": "2019-01-29 21:13"},
        {"id": "7A0", "data": "FFCDCCAA", "timestamp": "2019-01-29 21:13"},
        {"id": "711", "data": "ABCF", "timestamp": "2019-01-29 21:13"}
        ]
    for dataPoint in sampleWSData:
        print(sampleParser.parse_single_data(dataPoint, convert=True))

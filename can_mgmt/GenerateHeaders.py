import pandas as pd
import datetime as dt

# Name of the column with "C-friendly" names
name_column = "name"

sensors_df = pd.read_csv("SensorDict.csv", sep=",", header=0, dtype="str")
savefile = open("CANID.h", "w+")

header = "/* Generated on " + str(dt.datetime.now()) + "\n"
header += "* This file contains all of the constants that are\n"
header += "* being used on the CAN bus.\n"
header += "*\n"
header += "* Each message has an ID with specified sensors that\n"
header += "* lie on each message from bytes *_START_BYTE to\n"
header += "* *_END_BYTE.\n*/\n\n"
header += "#ifndef CANID_H\n#define CANID_H"

savefile.write(header)

lastID = ""
for row in range(0, len(sensors_df)):
    sensor_name_and_type = sensors_df.loc[row, name_column]
    last_underscore = sensor_name_and_type[::-1].find("_")
    assert last_underscore != -1, "Names not formatted correctly"
    sensor_name = sensor_name_and_type[0:len(sensor_name_and_type) - 1 -
                                       last_underscore]  # i.e. "ACCEL"
    ID = sensors_df.loc[row, "id"]
    if lastID != ID:
        savefile.write("\n#define " + sensor_name + "_CAN_ID " + ID + "\n")
    savefile.write("#define " + sensor_name_and_type + "_START_BYTE " +
                   sensors_df.loc[row, "MSB"] + "\n")
    savefile.write("#define " + sensor_name_and_type + "_END_BYTE " +
                   sensors_df.loc[row, "LSB"] + "\n")
    lastID = ID
savefile.write("#endif /* CANID_H */")
savefile.close()

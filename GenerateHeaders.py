import pandas as pd

# Name of the column with "C-friendly" names
name_column = "name"

sensors_df = pd.read_csv("SensorDict.csv", sep=",", header=0, dtype="str")
savefile = open("CANID.h", "w+")

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
savefile.close()

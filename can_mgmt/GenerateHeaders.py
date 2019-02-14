import pandas as pd
import datetime as dt

sensors_df = pd.read_csv("SensorDict.csv", sep=",", header=0, dtype="str")
savefile = open("CANID.h", "w+")

header = """/* Generated on {}
* This file contains all of the constants that are
* being used on the CAN bus.
*
* Each message has an ID with specified sensors that
* lie on each message from bytes *_START_BYTE to
* *_END_BYTE.
*/

#ifndef CANID_H
#define CANID_H""".format(str(dt.datetime.now()))

savefile.write(header)

last_ID = ""
for index, row in sensors_df.iterrows():
    sensor_name_and_type = row["name"]
    last_underscore = sensor_name_and_type.rindex("_")
    assert last_underscore != -1, "Names not formatted correctly"
    sensor_name = sensor_name_and_type[0:last_underscore]
    ID = row["id"]
    if last_ID != ID:
        savefile.write("\n#define {}_CAN_ID {}\n".format(sensor_name, ID))
    savefile.write("#define {}_START_BYTE {}\n".format(sensor_name_and_type,
                                                       row["MSB"]))
    savefile.write("#define {}_END_BYTE {}\n".format(sensor_name_and_type,
                                                     row["LSB"]))
    last_ID = ID

savefile.write("#endif /* CANID_H */")
savefile.close()

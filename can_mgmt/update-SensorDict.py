import requests
import pandas as pd
import datetime as dt

SPREADSHEET_FILE_ID = "195Y2cf9C2mrA6QCLuLJv3NHsCqTLi-3Wd07q4T5rXuM"
OUTPUT_CSV_FILE = "can_mgmt/SensorDict.csv"
OUTPUT_HEADER_FILE = "can_mgmt/CANID.h"
# Rows before the header are skipped.
# The row after the header will also be skipped because it is an example row.
HEADER_ROW = 5
BYTES_LIST = ["BYTE0", "BYTE1", "BYTE2", "BYTE3",
              "BYTE4", "BYTE5", "BYTE6", "BYTE7"]
BITS_DICT = {"BYTE0": (7, 0), "BYTE1": (15, 8), "BYTE2": (23, 16),
             "BYTE3": (31, 24), "BYTE4": (39, 32), "BYTE5": (47, 40),
             "BYTE6": (55, 48), "BYTE7": (63, 56)}

# This only gets the FIRST SHEET in the document
# If there is more than one sheet, make sure the first sheet is correct
response = requests.get("https://docs.google.com/spreadsheet/ccc?key=" +
                        SPREADSHEET_FILE_ID + "&output=csv")
# Check that status code = 200
response.raise_for_status()

# The CSV spreadsheet is requests.content
# Turn it into file:
savefile_csv = open(OUTPUT_CSV_FILE, "wb")
savefile_csv.write(response.content)
savefile_csv.close()

# Read file as dataframe.
content_df = pd.read_csv(OUTPUT_CSV_FILE, sep=",", header=HEADER_ROW,
                         dtype="str")

# Drop unwanted columns:
content_df = content_df.drop(["TRANSMITTING MODULE", "DESCRIPTION / SENSOR",
                              "AddMethd"], axis="columns")

# Drop example row:
# content_df = content_df.drop(0)
content_df = content_df.set_index("ID", drop=True)

# New dataframe for output
output_df = pd.DataFrame(None, columns=["id", "MSB", "LSB", "name"])
flags_df = pd.DataFrame(None, columns=["id", "MSB", "LSB", "name"])

for index, row in content_df.iterrows():
    last_cell = None
    for column in BYTES_LIST:
        item = str(row[column])
        # Mediocre check that the names are formatted correctly:
        if item.find("\n") != -1:
            flags_list = item.split("\n")
            for flag_i, flag in enumerate(flags_list):
                flag_paren_start = flag.find("(")
                flag_bit = str(int(flag[flag_paren_start + 1]) +
                                   8 * int(column[4]))
                flag = flag[0:flag_paren_start - 1]
                flags_df = flags_df.append({"id": index.upper(), "MSB": flag_bit,
                                           "LSB": flag_bit, "name": flag},
                                           ignore_index=True)
            continue
        paren_start = item.find("(")
        if item.find("_") == -1:
            break
        # Get the most sig. bit and least sig. bit i.e. (7:0)
        msb, lsb = BITS_DICT[column]
        # Remove all text after opening parenthesis
        if paren_start != -1:
            item = item[0:paren_start-1]
        # When two adjacent bytes are the same ID, let lsb = current lsb
        if(item == last_cell):
            output_df.at[output_df.index[-1], "MSB"] = str(msb)
        # Otherwise create new row in the csv with the bit numbers
        else:
            output_df = output_df.append({"id": index, "MSB": msb,
                                          "LSB": lsb, "name": item},
                                         ignore_index=True)
        last_cell = item

# Save new output file.
output_df = output_df.append(flags_df, ignore_index=True)
output_df.to_csv(OUTPUT_CSV_FILE, index=None, header=True)
savefile_h = open(OUTPUT_HEADER_FILE, "w+")

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

savefile_h.write(header)

last_ID = ""
for index, row in output_df.iterrows():
    sensor_name_and_type = row["name"]
    ID = row["id"]
    # If it does not find underscore, then it will be treated as a flag
    if sensor_name_and_type.find("FLAG") != -1:
        if last_ID != ID:
            savefile_h.write("\n")
        savefile_h.write("#define {}_BIT {}\n".format(sensor_name_and_type,
                                                      row["LSB"]))
        last_ID = ID
        continue
    last_underscore = sensor_name_and_type.rindex("_")
    sensor_name = sensor_name_and_type[0:last_underscore]
    if last_ID != ID:
        savefile_h.write("\n#define {}_CAN_ID {}\n".format(sensor_name, ID))
    savefile_h.write("#define {}_START_BIT {}\n".format(sensor_name_and_type,
                                                        row["LSB"]))
    savefile_h.write("#define {}_END_BIT {}\n".format(sensor_name_and_type,
                                                      row["MSB"]))
    last_ID = ID

savefile_h.write("#endif /* CANID_H */")
savefile_h.close()

import requests
import pandas as pd
import datetime as dt

SPREADSHEET_FILE_ID = "195Y2cf9C2mrA6QCLuLJv3NHsCqTLi-3Wd07q4T5rXuM"
OUTPUT_CSV_FILE = "SensorDict.csv"
OUTPUT_HEADER_FILE = "CANID.h"
# Rows before the header are skipped.
# The row after the header will also be skipped because it is an example row.
HEADER_ROW = 5
BYTES_LIST = ["BYTE0", "BYTE1", "BYTE2", "BYTE3",
              "BYTE4", "BYTE5", "BYTE6", "BYTE7"]

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

for index, row in content_df.iterrows():
    last_cell = None
    for column in BYTES_LIST:
        item = str(row[column])
        # Mediocre check that the names are formatted correctly:
        if(item.find("_") == -1):
            break
        paren_start = item.find("(")
        # If there is an opening parenthesis, remove all text after it
        if(paren_start != -1):
            item = item[0:paren_start-1]
        # When two adjacent bytes are the same, increment least sig. byte
        if(item == last_cell):
            new_lsb = int(output_df.loc[output_df.index[-1], "LSB"]) + 1
            output_df.at[output_df.index[-1], "LSB"] = str(new_lsb)
        # Otherwise create new row in the csv with the byte number
        else:
            byte_num = column[4]
            output_df = output_df.append({"id": index, "MSB": byte_num,
                                          "LSB": byte_num, "name": item},
                                         ignore_index=True)
        last_cell = item

# Save new output file.
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
    last_underscore = sensor_name_and_type.rindex("_")
    sensor_name = sensor_name_and_type[0:last_underscore]
    ID = row["id"]
    if last_ID != ID:
        savefile_h.write("\n#define {}_CAN_ID {}\n".format(sensor_name, ID))
    savefile_h.write("#define {}_START_BYTE {}\n".format(sensor_name_and_type,
                                                         row["MSB"]))
    savefile_h.write("#define {}_END_BYTE {}\n".format(sensor_name_and_type,
                                                       row["LSB"]))
    last_ID = ID

savefile_h.write("#endif /* CANID_H */")
savefile_h.close()

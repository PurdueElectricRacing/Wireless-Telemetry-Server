import requests
import pandas as pd
import math
# Maybe you can do this with the csv library
# But Pandas is way easier to use

file_id = "195Y2cf9C2mrA6QCLuLJv3NHsCqTLi-3Wd07q4T5rXuM"
output_file = "SavedGoogleDrive.csv"
# Index of the header row:
ignore_rows = 5

# This only gets the FIRST SHEET in the document
# If there is more than one sheet, make sure the first sheet is correct
response = requests.get("https://docs.google.com/spreadsheet/ccc?key=" +
                        file_id + "&output=csv")
# Check that status code = 200
response.raise_for_status()

# The CSV spreadsheet is requests.content
# Turn it into file:
savefile = open(output_file, "wb")
savefile.write(response.content)
savefile.close()

# Read file as dataframe.
content_df = pd.read_csv(output_file, sep=",", header=ignore_rows, dtype="str")

# Drop unwanted columns:
content_df = content_df.drop(["TRANSMITTING MODULE", "DESCRIPTION / SENSOR",
                              "AddMethd"], axis="columns")

bytes_list = ["BYTE0", "BYTE1", "BYTE2", "BYTE3",
              "BYTE4", "BYTE5", "BYTE6", "BYTE7"]

# Drop example row:
content_df = content_df.drop(0)
content_df = content_df.set_index("ID", drop=False)

# New dataframe for output
output_df = pd.DataFrame(None, columns=["id", "MSB", "LSB", "name"])

# Now iterate through each cell
for row in content_df["ID"]:
    lastcell = None

    if row != row:
        print("Unable to parse " + str(row))
        continue

    for column in bytes_list:
        item = str(content_df.loc[row, column])
        # Ignore bytes with no assigned name
        if(item == "nan"):
            continue
        # Find location of parenthesis
        paren_start = item.find("(")
        # If there is an opening parenthesis, remove all text after it
        if(paren_start != -1):
            item = item[0:paren_start-1]
        # When two adjacent bytes are the same, increment least sig. byte
        if(item == lastcell):
            new_lsb = int(output_df.loc[output_df.index[-1], "LSB"]) + 1
            output_df.at[output_df.index[-1], "LSB"] = str(new_lsb)
        # Otherwise create new row in the csv with the byte number
        else:
            byte_num = column[4]
            output_df = output_df.append({"id": row, "MSB": byte_num,
                                          "LSB": byte_num, "name": item},
                                         ignore_index=True)
        lastcell = item
# Save new output file.
output_df.to_csv(output_file, index=None, header=True)

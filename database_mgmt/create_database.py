import os
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

sensor_dict = pd.read_csv("../can_mgmt/SensorDict.csv", header=0,  dtype="str")

db = Database()
cursor = db.get_cursor()
cursor.execute("CREATE DATABASE sensors")
cursor.execute("USE sensors")

current_id = "#####"
for index, row in sensor_dict.iterrows():
    if row["id"][3] == current_id[3]:
        add_query = "ADD COLUMN {} INT(16) NULL".format(row["name"])
        cursor.execute(add_query)
    else:
        current_id = row["id"]
        table_name = current_id[0:3]
        create_query = "CREATE TABLE {}".format(table_name)
        alter_query = "ALTER TABLE {}".format(table_name)
        timestamp_query = "ADD COLUMN timestamp DATETIME NOT NULL"
        add_query = "ADD COLUMN {} INT(16) NULL".format(row["name"])
        cursor.execute(create_query)
        cursor.execute(alter_query)
        cursor.execute(timestamp_query)
        cursor.execute(add_query)

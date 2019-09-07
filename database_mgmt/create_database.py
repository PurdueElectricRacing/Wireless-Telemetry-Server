import os
import pandas as pd
from database import Database

sensor_dict = pd.read_csv('can_mgmt/SensorDict.csv', header=0,  dtype='str')

db = Database()
cursor = db.get_cursor()
cursor.execute('CREATE DATABASE sensors')
cursor.execute('USE sensors')

current_id = '#####'
for index, row in sensor_dict.iterrows():
    if row['id'][3] == current_id[3]:
        db.add_column(current_id[1:4], row['name'], 'INT(16) NULL')
    else:
        current_id = row['id']
        # Tables can't start with a 0x (no starting integer), so start with x
        table_name = current_id[1:4]
        db.create_table(table_name)
        db.add_column(table_name, row['name'], 'INT(16) NULL')

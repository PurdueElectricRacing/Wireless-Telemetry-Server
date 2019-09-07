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
        add_query = 'ALTER TABLE {} ADD COLUMN {} INT(16) NULL'.format(current_id[1:4], row['name'])
        cursor.execute(add_query)
    else:
        current_id = row['id']
        table_name = current_id[1:4] # Tables can't start with a 0x (no starting integer), so start with x instead
        create_query = 'CREATE TABLE {} (timestamp DATETIME(3) NOT NULL)'.format(table_name)
        alter_query = 'ALTER TABLE {} ADD COLUMN {} INT(16) NULL'.format(table_name, row['name'])
        cursor.execute(create_query)
        cursor.execute(alter_query)

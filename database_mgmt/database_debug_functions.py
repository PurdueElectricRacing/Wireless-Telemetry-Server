import os
import sys
from database import Database

setting = sys.argv[1]

if setting == 'wipe':
    db = Database()
    cursor = db.get_cursor()
    cursor.execute("DROP DATABASE sensors")

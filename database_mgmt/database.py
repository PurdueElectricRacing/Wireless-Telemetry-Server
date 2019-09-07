import os
import mysql.connector
from dotenv import load_dotenv
load_dotenv()


class Database:
    def __init__(self):
        self.host = os.getenv('DATABASE_HOST')
        self.user = os.getenv('DATABASE_USER')
        self.password = os.getenv('DATABASE_PASSWORD')
        self._connection = None

    def connect(self):
        db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )

        # Set a connection so that a new connection doesn't
        # have to be created for every new test
        self._connection = db

        return db

    def get_cursor(self):
        if self._connection is None:
            self.connect()

        return self._connection.cursor()

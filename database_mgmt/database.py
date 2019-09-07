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

    def require_connection(func):
        def wrapper(*args):
            self = args[0]
            if self._connection is None:
                self.connect()
            return func(*args)
        return wrapper

    @require_connection
    def get_cursor(self):
        return self._connection.cursor()

    @require_connection
    def create_table(self, table):
        cursor = self.get_cursor()
        create_query = f'CREATE TABLE {table} (timestamp DATETIME(3) NOT NULL)'
        cursor.execute(create_query)


    @require_connection
    def add_column(self, table, column, data_type):
        cursor = self.get_cursor()
        alter_query = f'ALTER TABLE {table} ADD COLUMN {column} {data_type}'
        cursor.execute(alter_query)

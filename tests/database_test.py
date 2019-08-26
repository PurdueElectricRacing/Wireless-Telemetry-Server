import mysql.connector

class DatabaseTest:

    # Ensure the connection can be made to the database
    def test_connection(self):
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=""
            )

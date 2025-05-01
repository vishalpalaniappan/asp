import time
import mysql.connector
import sys

class DatabaseWriter:

    def __init__(self):
        self.connect()
        self.createSystemsTable()


    def connect(self):
        '''
            Connect to the database.
        '''
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="random-password",
            database="aspDatabase",
            port="3306"
        )

        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT version();")

        dbVersion = self.cursor.fetchone()[0]
        print(f"DB Version: {dbVersion}")

    def createSystemsTable(self):
        '''
            Create the table to store all the systems.
        '''
        sql = '''
            CREATE TABLE IF NOT EXISTS SYSTEMSTABLE (
                id INT AUTO_INCREMENT PRIMARY KEY,
                system_id VARCHAR(100) NOT NULL,
                system_ver VARCHAR(100),
                name VARCHAR(100),
                description VARCHAR(100),
                programs JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
        '''

        self.cursor.execute(sql)



if __name__ == "__main__":
    a = DatabaseWriter()
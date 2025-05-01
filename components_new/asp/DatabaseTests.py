import time
import mysql.connector
import sys
import json

class DatabaseWriter:

    def __init__(self):
        self.connect()
        self.createSystemsTable()
        self.addSystem()


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


    def addSystem(self):
        programs = json.dumps({"A":1})
        sql = ''' INSERT INTO SYSTEMSTABLE(system_id, system_ver, name, description, programs)
                VALUES(%s,%s,%s,%s,%s) '''
        self.cursor.execute(sql, ("1234", "0.0.1", "Distributed Sorting System", "desc", programs))
        self.conn.commit()



if __name__ == "__main__":
    a = DatabaseWriter()
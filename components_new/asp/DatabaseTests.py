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
            CREATE TABLE IF NOT EXISTS SYSTEMSTABLE 
            (
                id INT AUTO_INCREMENT PRIMARY KEY,
                system_id VARCHAR(100) NOT NULL,
                system_ver VARCHAR(100),
                name VARCHAR(100),
                description VARCHAR(100),
                programs JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.cursor.execute(sql)

    def addSystem(self):
        system_id = "1234"
        system_ver = "0.0.1".replace(".","")
        name = "Distributed Sorting System"
        description = "System Description"
        programs = json.dumps({"A":1})

        sql = ''' INSERT INTO SYSTEMSTABLE(system_id, system_ver, name, description, programs)
                VALUES(%s,%s,%s,%s,%s) '''
        self.cursor.execute(sql, (system_id, system_ver, name, description, programs))
        self.conn.commit()

        sql = f'''
            CREATE TABLE IF NOT EXISTS {system_id}_{system_ver}_traces 
            (
                id INT AUTO_INCREMENT PRIMARY KEY,
                deployment_id VARCHAR(100) NOT NULL,
                trace_id VARCHAR(100),
                start_ts TIMESTAMP,
                end_ts TIMESTAMP,
                trace_type VARCHAR(100),
                traces TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.cursor.execute(sql)





if __name__ == "__main__":
    a = DatabaseWriter()
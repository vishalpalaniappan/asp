import time
import mysql.connector
import sys
import json
from DbConn import DBClient

class DatabaseWriter:

    def __init__(self):
        with DBClient() as db:
            self.conn = db.conn
            self.cursor = db.cursor
            self.createSystemsTable()
            self.addSystem()
            self.addDeployments("1234","0.0.1","9999", None)

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

    def addDeployments(self, system_id, system_ver, deployment_id, startTs):
        system_ver = system_ver.replace(".","")
        tableName = f"{system_id}_{system_ver}_deployments"

        sql = f''' INSERT INTO {tableName}(deployment_id, start_ts, end_ts)
                VALUES(%s,%s,%s) '''
        self.cursor.execute(sql, (deployment_id, startTs, None))
        self.conn.commit()


    def addSystem(self):
        system_id = "1234"
        system_ver = "0.0.1"
        name = "Distributed Sorting System"
        description = "System Description"
        programs = json.dumps({"A":1})

        sql = ''' INSERT INTO SYSTEMSTABLE(system_id, system_ver, name, description, programs)
                VALUES(%s,%s,%s,%s,%s) '''
        self.cursor.execute(sql, (system_id, system_ver, name, description, programs))
        self.conn.commit()

        system_ver = system_ver.replace(".","")

        sql = f'''
            CREATE TABLE IF NOT EXISTS {system_id}_{system_ver}_deployments 
            (
                id INT AUTO_INCREMENT PRIMARY KEY,
                deployment_id VARCHAR(100) NOT NULL,
                start_ts TIMESTAMP,
                end_ts TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.cursor.execute(sql)

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
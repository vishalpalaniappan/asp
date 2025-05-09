import time
import mysql.connector
import sys
import json
from DbConn import DBClient

class IOEventsTest:

    def __init__(self):
        with DBClient() as db:
            self.conn = db.conn
            self.cursor = db.cursor
            self.createIoEventsTable()

    def createIoEventsTable(self):
        '''
            Create the table to store all the systems.
        '''
        sql = '''
            CREATE TABLE IF NOT EXISTS IOEVENTS 
            (
                id INT AUTO_INCREMENT PRIMARY KEY,
                system_id VARCHAR(100) NOT NULL,
                system_ver VARCHAR(100),
                deployment_id VARCHAR(100),
                program_execution_id VARCHAR(100),
                start_ts TIMESTAMP,
                end_ts TIMESTAMP,
                adli_execution_id VARCHAR(100),
                adli_execution_index VARCHAR(100),
                trace_type VARCHAR(100),
                node TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.cursor.execute(sql)

if __name__ == "__main__":
    a = IOEventsTest()
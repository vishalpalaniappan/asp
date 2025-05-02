import sqlite3
import json
import os
from datetime import datetime

class EventWriter:
    '''
        This class writes the IO events to the database. 
    '''

    def __init__(self, db):
        self.conn = db.conn
        self.cursor = self.conn.cursor()
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

    def checkIfFieldExists(self, table, column, value):
        '''
            Checks if the database has the given field.
        '''
        query = f"""
            SELECT 1 FROM {table}
            WHERE {column} = %s
            LIMIT 1
        """
        self.cursor.execute(query, (value, ))

        return True if self.cursor.fetchone() else False
        
    def addEventsToDb(self, logFile):
        '''
            Add system io events to the database.
        '''
        sysId = logFile.decoder.header.sysinfo["metadata"]["systemId"]
        sysVer = logFile.decoder.header.sysinfo["metadata"]["systemVersion"]
        deploymentId = logFile.decoder.header.sysinfo["adliSystemExecutionId"]
        programId = logFile.decoder.header.execInfo["programExecutionId"]
        ts = logFile.decoder.header.execInfo["timestamp"]
        programInfo = logFile.decoder.header.programInfo
        
        # If the program has already been processed, then return.
        fileExists = self.checkIfFieldExists("IOEVENTS", "program_execution_id", programId)
        if (fileExists):
            print(f"File {programId} has already been processed.")
            return

        # Create table data for each io node
        event_data = []
        for event in logFile.decoder.systemIoNodes:
            node = event["node"]
            adliExecutionId = node["adliExecutionId"]
            adliExecutionIndex = node["adliExecutionIndex"]
            trace_type = event["type"]
            nodeStr = json.dumps(node)
            dt_string = datetime.fromtimestamp(float(ts))
            event_data.append((sysId, sysVer, deploymentId, programId, dt_string, None, adliExecutionId, adliExecutionIndex, trace_type, nodeStr))        


        sql = f''' INSERT INTO IOEVENTS(
            system_id, system_ver, deployment_id, \
            program_execution_id, start_ts, end_ts, \
            adli_execution_id, adli_execution_index, \
            trace_type, node
            )
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
        self.cursor.executemany(sql, event_data)
        self.conn.commit()
        
        print(f"Added System IO events from {programInfo['name']} to database.")
import sqlite3
import json

class EventWriter:
    '''
        This class writes the IO events to the database. 
    '''

    def __init__(self, db_path="ioEvents.db"):
        try:
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS IOEVENTS
                (system_id string, sys_ver string, deployment_id string, program_execution_id  string, ts real, adli_execution_id string,\
                                 adli_execution_index int, type string, node string)''')
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise

    def __enter__(self):
        return self 
 
    def __exit__(self):
        '''
            Close the database connection on exit.
        '''
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    def checkIfFieldExists(self, table, column, value):
        '''
            Checks if the database has the given field.
        '''
        query = f'SELECT {column} FROM {table} WHERE {column} = ?' 
        self.cursor.execute(query, [value])
        row = self.cursor.fetchone() 
        return row is not None
        
    def addEventsToDb(self, logFile):
        '''
            Add system io events to the database.
        '''
        sysId = logFile.decoder.header.sysinfo["metadata"]["systemId"]
        sysVer = logFile.decoder.header.sysinfo["metadata"]["systemVersion"]
        deploymentId = logFile.decoder.header.sysinfo["adliSystemExecutionId"]
        programId = logFile.decoder.header.execInfo["programExecutionId"]
        ts = float(logFile.decoder.header.execInfo["timestamp"])
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
            type = event["type"]
            nodeStr = json.dumps(node)
            event_data.append([sysId, sysVer, deploymentId, programId, ts, adliExecutionId, adliExecutionIndex, type, nodeStr])        

        # Execute SQL statement
        sql = ''' INSERT OR REPLACE INTO IOEVENTS(system_id, sys_ver, deployment_id, program_execution_id, ts, adli_execution_id,\
              adli_execution_index, type, node)
            VALUES(?,?,?,?,?,?,?,?,?) '''
        self.cursor.executemany(sql, event_data)
        self.conn.commit()
        
        print(f"Added System IO events from {programInfo['name']} to database.")
import sqlite3
import json
import math

class EventWriter:

    def __init__(self):
        
        self.conn = sqlite3.connect("ioEvents.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS IOEVENTS
            (system_id string, sys_ver string, deployment_id string, program_id string, ts date, execution_id string, execution_index int, type string, node string)''')
        self.conn.commit()
        
    def addEventsToDb(self, logFile):

        sysId = logFile.decoder.header.sysinfo["metadata"]["systemId"]
        sysVer = logFile.decoder.header.sysinfo["metadata"]["systemVersion"]
        deploymentId = logFile.decoder.header.sysinfo["adliSystemExecutionId"]
        programId = logFile.decoder.header.execInfo["programExecutionId"]
        ts = math.floor(float(logFile.decoder.header.execInfo["timestamp"]))

        print(logFile.decoder.header.execInfo)
        event_data = []
        for event in logFile.decoder.systemIoNodes:
            node = event["node"]
            execId = node["adliExecutionId"]
            execIndex = node["adliExecutionIndex"]
            type = event["type"]
            nodeStr = json.dumps(node)
            event_data.append([sysId, sysVer, deploymentId, programId, ts, execId, execIndex, type, nodeStr])

        sql = ''' INSERT OR REPLACE INTO IOEVENTS(system_id, sys_ver, deployment_id, program_id, ts, execution_id, execution_index, type, node)
            VALUES(?,?,?,?,?,?,?,?,?) '''
        self.cursor.executemany(sql, event_data)
        self.conn.commit()
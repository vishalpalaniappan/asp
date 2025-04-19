import sqlite3
import json

class SysWriter:

    def __init__(self):        
        self.conn = sqlite3.connect("asp.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS SYSTEMTABLES
            (system_id int, version real, name text, description, programs)''')
        self.conn.commit()
        
    def write_file(self, cdlFile):
        '''
            Writes CDL file to database.
            1. Add system to SYSTEMTABLES
            2. Create tables for programs, deployments and traces
            3. Add filetree for system for this program
            4. Add extracted unique traces to the table.
        '''
        self.addToSystemIndex(cdlFile.decoder.header.sysinfo)
        self.createTables(cdlFile.decoder.header)

    def createTables(self, header):
        sysId = header.sysinfo["metadata"]["systemId"]        
        sysVer = header.sysinfo["metadata"]["systemVersion"]

        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {sysId}_{sysVer}_deployments
            (deployment_id string, ts real)''')
        self.conn.commit()

        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS {sysId}_{sysVer}_programs
            (name string, description string, language string, fileTree string)''')
        self.conn.commit()

        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS {sysId}_{sysVer}_traces
            (deployment_id string, trace_id string, startTs real, endTs real, traceType string)''')
        self.conn.commit()


    def addToSystemIndex(self, systemInfo):
        '''
            Adds sys info to SYSTEMTABLES and creates tables for programs, deployments and traces.
        '''
        sysId = systemInfo["metadata"]["systemId"]        
        sysVer = systemInfo["metadata"]["systemVersion"]
        name = systemInfo["metadata"]["name"]
        description = systemInfo["metadata"]["description"]
        programs = json.dumps(systemInfo["programs"])

        self.cursor.execute(f'''
            SELECT system_id FROM SYSTEMTABLES WHERE system_id = {sysId} and version = {sysVer}
        ''')
        rows = self.cursor.fetchall()

        # If entry for specified system id and version doesn't exist, add it.
        if (len(rows) == 0):
            sql = ''' INSERT INTO SYSTEMTABLES(system_id, version, name, description, programs)
                VALUES(?,?,?,?,?) '''
            self.cursor.execute(sql, [sysId, sysVer, name, description, programs])
            self.conn.commit()

        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{sysId}-{sysVer}-programs"
            (id int, name string, description string, language string, fileTree string)''')

        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{sysId}-{sysVer}-deployments"
            (deployment_id int, ts date)''')

        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{sysId}-{sysVer}-traces"
            (deployment_id int, trace_id int, startTs date, endTs date, fileTree string)''')
        self.conn.commit()

        

if __name__ == "__main__":
    a = SysWriter()
    
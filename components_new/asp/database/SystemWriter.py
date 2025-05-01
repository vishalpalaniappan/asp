import sqlite3
import json
import os

class SystemWriter:
    '''
        Given a CDL file, this program writes the metadata related to the 
        CDL file to the database. This includes, the programs, deployments
        and assembled traces.
    '''

    def __init__(self):
        path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        db_path = os.path.join(path, "asp.db")
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS SYSTEMTABLES
            (system_id string, version string, name string, description text, programs string,
                PRIMARY KEY (system_id, version))
            '''
        )
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
        self.addPrograms(cdlFile.decoder.header)
        self.addDeployments(cdlFile.decoder.header)

    def checkIfFieldExists(self, table, column, value):
        '''
            Checks if the database has the given field.
        '''
        query = f'SELECT {column} FROM "{table}" WHERE {column} = ?' 
        self.cursor.execute(query, [value])
        row = self.cursor.fetchone() 
        return row is not None
    
    def addDeployments(self, header):
        '''
            Add deployments to the database.
        '''
        sysId = header.sysinfo["metadata"]["systemId"]        
        sysVer = header.sysinfo["metadata"]["systemVersion"]
        TABLENAME = f"{sysId}_{sysVer}_deployments"

        deploymentId = header.sysinfo["adliSystemExecutionId"]
        
        # Return if the deployment id has already been written to the database
        hasName = self.checkIfFieldExists(TABLENAME, "deployment_id", deploymentId)
        if (hasName):
            return

        sql = f''' INSERT OR REPLACE INTO "{TABLENAME}"(deployment_id)
                VALUES(?) '''
        self.cursor.execute(sql, [deploymentId])
        self.conn.commit()


    def addPrograms(self, header):
        '''
            Add programs to the database.
        '''
        sysId = header.sysinfo["metadata"]["systemId"]        
        sysVer = header.sysinfo["metadata"]["systemVersion"] 
        programInfo = header.programInfo
        
        TABLENAME = f"{sysId}_{sysVer}_programs"

        name = programInfo["name"]
        description = programInfo["description"]
        language = programInfo["language"]
        fileTree = json.dumps(header.fileTree)

        # Return if the program has already been written to the database
        hasName = self.checkIfFieldExists(TABLENAME, "name", name)
        if (hasName):
            return

        sql = f''' INSERT OR REPLACE INTO "{TABLENAME}"(name, description, language, file_tree)
                VALUES(?,?,?,?) '''
        self.cursor.execute(sql, [name, description, language, fileTree])
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
            SELECT system_id FROM SYSTEMTABLES WHERE system_id = ? and version = ?
        ''', (sysId, sysVer))
        entry = self.cursor.fetchone()

        # If entry for specified system id and version doesn't exist, add it.
        if (entry is None):
            sql = ''' INSERT INTO SYSTEMTABLES(system_id, version, name, description, programs)
                VALUES(?,?,?,?,?) '''
            self.cursor.execute(sql, [sysId, sysVer, name, description, programs])
            self.conn.commit()

        table_name = f"{sysId}_{sysVer}_deployments"
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{table_name}"
            (deployment_id string, PRIMARY KEY (deployment_id))''')
        
        table_name = f"{sysId}_{sysVer}_programs"
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{table_name}"
            (name string PRIMARY KEY, description string, language string, file_tree string)''')
        
        table_name = f"{sysId}_{sysVer}_traces"
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{table_name}"
            (deployment_id string, trace_id string, start_ts real, end_ts real, 
             trace_type string, traces string, PRIMARY KEY (deployment_id, trace_id))''')
        self.conn.commit()
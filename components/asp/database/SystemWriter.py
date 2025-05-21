import sqlite3
import json
import os

class SystemWriter:
    '''
        Given a CDL file, this program writes the metadata related to the 
        CDL file to the database. This includes, the programs, deployments
        and assembled traces.
    '''

    def __init__(self, db):
        self.conn = db.conn
        self.cursor = self.conn.cursor()

        sql = '''
            CREATE TABLE IF NOT EXISTS SYSTEMSTABLE 
            (
                id INT AUTO_INCREMENT PRIMARY KEY,
                system_id VARCHAR(100) NOT NULL,
                system_ver VARCHAR(100),
                name VARCHAR(100),
                description TEXT,
                programs JSON,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''
        self.cursor.execute(sql)
        
    def write_file(self, cdlFile):
        '''
            Writes CDL file to database.
            1. Add system to SYSTEMTABLES
            2. Create tables for programs, deployments and traces
            3. Add filetree for system for this program
            4. Add extracted unique traces to the table.
        '''
        self.addToSystemIndex(cdlFile.decoder.header)
        self.addDeployments(cdlFile.decoder.header)

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
    
    def addDeployments(self, header):
        '''
            Add deployments to the database.
        '''
        deployment_id = header.sysinfo["adliSystemExecutionId"]
        
        
        if header.sysinfo and "metadata" in header.sysinfo and header.sysinfo["metadata"]:
            system_id = header.sysinfo["metadata"]["systemId"] if "systemId" in header.sysinfo["metadata"] else None
            system_ver = header.sysinfo["metadata"]["systemVersion"] if "systemId" in header.sysinfo["metadata"] else None
            system_ver = system_ver.replace(".","")
        else:
            system_id = None
            system_ver = None
        
        tableName = f"{system_id}_{system_ver}_deployments"

        # Return if the program has already been written to the database
        hasName = self.checkIfFieldExists(tableName, "deployment_id", deployment_id)
        if (hasName):
            return

        sql = f''' INSERT INTO {tableName}(deployment_id, start_ts, end_ts)
                VALUES(%s,%s,%s) '''
        self.cursor.execute(sql, (deployment_id, None, None))
        self.conn.commit()


    def addToSystemIndex(self, header):
        '''
            Adds sys info to SYSTEMTABLES and creates tables for programs, deployments and traces.
        '''
        systemInfo = header.sysinfo
        if systemInfo and "metadata" in systemInfo and header.sysinfo["metadata"]:
            system_id = header.sysinfo["metadata"]["systemId"] if "systemId" in header.sysinfo["metadata"] else None
            system_ver = header.sysinfo["metadata"]["systemVersion"] if "systemId" in header.sysinfo["metadata"] else None
            name = systemInfo["metadata"]["name"]
            description = systemInfo["metadata"]["description"]
        else:
            system_id = None
            system_ver = None
            name = None
            description = None
            
        programs = json.dumps(header.fileTree)

        query = f"""
            SELECT 1 FROM SYSTEMSTABLE
            WHERE system_id = %s AND system_ver = %s
        """
        self.cursor.execute(query, (system_id,system_ver))
        systemExists = True if self.cursor.fetchone() else False
        if (systemExists):
            return

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
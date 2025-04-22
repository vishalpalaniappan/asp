import sqlite3
import os

class SystemDatabaseReader:
    '''
        This class will perform queries on the ASP database and return
        the results.
    '''

    def __init__(self):
        self.openConnections()

    def openConnections(self):
        '''
            Initialize the database connections.
        '''
        path = os.path.dirname(os.path.dirname(__file__))
        aspPath = os.path.join(path, "asp.db")
        try:
            self.aspConn = sqlite3.connect(aspPath)
            self.aspCursor = self.aspConn.cursor()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise

    def closeConnections(self):
        '''
            Close the database connections.
        '''
        if hasattr(self, 'aspConn'):
            self.aspConn.close()

    def __del__(self):
        '''
            Clean up database connections.
        '''
        self.closeConnections()

    def checkIfTableExists(self, tableName):
        '''
            Check if the given table exists.
        '''
        query = f'PRAGMA table_info("{tableName}")' 
        self.aspCursor.execute(query)
        return self.aspCursor.fetchone()

    def getColumns(self, tableName):
        '''
            Get the columns for a table.
        '''
        query = f'PRAGMA table_info("{tableName}")' 
        self.aspCursor.execute(query)
        return self.aspCursor.fetchall()
    
    def addColumnNameToData(self, columns, data):
        '''
            Given the column names and the data, create 
            an object which uses the column names as key.
        '''
        obj = {}
        for index, columnValue in enumerate(data):
            obj[columns[index][1]] = columnValue
        return obj
    
    def getAllEntriesInTable(self, tableName):
        '''
            Given a table name, get all entries in the table.
        '''
        query = f'SELECT * FROM "{tableName}"'
        self.aspCursor.execute(query)
        rows = self.aspCursor.fetchall() 
        columns = self.getColumns(tableName)

        results = []
        for row in rows:
            results.append(self.addColumnNameToData(columns, row))

        return results
    
    def getSystems(self):
        '''
            Get all systems in the database.
        '''
        tableName = "SYSTEMTABLES"
        tableExists = self.checkIfTableExists(tableName=tableName)
        
        if (tableExists is None):
            return None

        return self.getAllEntriesInTable("SYSTEMTABLES")

    def getPrograms(self, systemId, systemVersion):     
        '''
            Get all programs given a system id and system version.
        '''   
        tableName = f"{systemId}_{systemVersion}_programs"
        tableExists = self.checkIfTableExists(tableName=tableName)

        if (tableExists is None):
            return None
        
        return self.getAllEntriesInTable(tableName)

    def getDeployments(self, systemId, systemVersion):  
        '''
            Get all the deployments for the given system.
        '''            
        tableName = f"{systemId}_{systemVersion}_deployments"
        tableExists = self.checkIfTableExists(tableName=tableName)

        if (tableExists is None):
            return None

        return self.getAllEntriesInTable(tableName)

    def getTraces(self, systemId, systemVersion, deploymentId):
        '''
            Get all the traces given a system id, version and deployment id.            
            # TODO: Add funtionality to filter traces by start and end timestamp.       
        '''
        tableName = f"{systemId}_{systemVersion}_traces"
        doesTableExist = self.checkIfTableExists(tableName=tableName)

        if (doesTableExist is None):
            return None

        query = f'SELECT * FROM "{tableName}" WHERE deployment_id = ?'
        self.aspCursor.execute(query, [deploymentId])
        rows = self.aspCursor.fetchall() 

        columns = self.getColumns(tableName)

        results = []
        for row in rows:
            results.append(self.addColumnNameToData(columns, row))

        return results
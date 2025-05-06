import mysql.connector
import os
import time
from datetime import datetime

class SystemDbReader:
    '''
        This class will perform queries on the ASP database and return
        the results.
    '''

    def __init__(self):
        self.conn = self.get_connection()
        self.cursor = self.conn.cursor()

    def close(self):
        """
            Close the database connection and cursor.
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def __del__(self):
        """
            Ensure resources are cleaned up when object is garbage collected.
        """
        self.close()

    def get_connection(self):
        
        isDocker = os.environ.get('IS_RUNNING_IN_DOCKER', False)

        if isDocker:
            host = "asp-mariadb-container"
        else:
            host = "localhost"

        MAX_ATTEMPTS = 20
        for attempt in range(MAX_ATTEMPTS):
            try:
                return mysql.connector.connect(
                    host= host,
                    user= "root",
                    password= "random-password",
                    database= "aspDatabase",
                    port= "3306",
                    autocommit=True 
                )
            except Exception as e:
                print(f"Attempt {attempt + 1}: {e}")
                print("Trying again in 5 seconds.")
                time.sleep(5)

        raise Exception(f"Tried to connect to database {attempt} times but failed.")
            
    def getColumns(self, tableName):
        '''
            Get the columns for a table.
        '''
        query = """
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = %s
        """

        with self.conn.cursor() as cursor:
            cursor.execute(query, (tableName,))
            result = cursor.fetchall()

        columns = []
        for row in result:
            columns.append(row[0])

        return columns
    
    def addColumnNameToData(self, columns, data):
        '''
            Given the column names and the data, create 
            an object which uses the column names as key.
        '''
        obj = {}
        for index, columnValue in enumerate(data):
            if isinstance(columnValue, datetime):
                obj[columns[index]] = columnValue.timestamp() * 1000
            else:
                obj[columns[index]] = columnValue

        return obj
    
    def getAllEntriesInTable(self, tableName):
        '''
            Given a table name, get all entries in the table.
        '''
        query = f'SELECT * FROM {tableName}'

        
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall() 

        columns = self.getColumns(tableName)

        results = []
        for row in rows:
            results.append(self.addColumnNameToData(columns, row))

        return results
    
    def getSystems(self):
        '''
            Get all systems in the database.
        '''
        return self.getAllEntriesInTable("SYSTEMSTABLE")

    def getDeployments(self, systemId, systemVersion):  
        '''
            Get all the deployments for the given system.
        '''            
        sysVerFormatted = systemVersion.replace(".","")
        tableName = f"{systemId}_{sysVerFormatted}_deployments"
        return self.getAllEntriesInTable(tableName)

    def getTraces(self, systemId, systemVersion, deploymentId):
        '''
            Get all the traces given a system id, version and deployment id.            
            # TODO: Add funtionality to filter traces by start and end timestamp.       
        '''
        sysVerFormatted = systemVersion.replace(".","")
        tableName = f"{systemId}_{sysVerFormatted}_traces"

        query = f'SELECT * FROM {tableName} WHERE deployment_id = %s'

        
        with self.conn.cursor() as cursor:
            cursor.execute(query, (deploymentId,))
            rows = cursor.fetchall() 

        columns = self.getColumns(tableName)

        results = []
        for row in rows:
            results.append(self.addColumnNameToData(columns, row))

        return results
    
if __name__ == "__main__":
    a = SystemDbReader()
    
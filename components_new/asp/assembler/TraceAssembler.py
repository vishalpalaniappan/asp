import sqlite3
import json
import os
from datetime import datetime

class TraceAssembler:
    '''
        This class is used to process the nodes in the ioEvents.db.
        For every start node, the system level trace is assembled.
        The assembled system level traces are written to the asp.db 
        database in the traces table for the given system.    
    '''

    def __init__(self, db):
        self.conn = db.conn
        self.cursor = db.conn.cursor()
        self.ioevent_cols = self.getColumns("IOEVENTS")
        self.processDatabase()

    def getColumns(self, tableName):
        '''
            Get the columns for a table.
        '''
        query = """
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = %s
        """
        self.cursor.execute(query, (tableName,))
        result = self.cursor.fetchall()

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
            obj[columns[index]] = columnValue

        return obj


    def processDatabase(self):
        '''
            Processes the database and extracts all the traces.
        '''
        # Get all the start nodes
        query = f'SELECT * FROM IOEVENTS WHERE trace_type = %s' 
        self.cursor.execute(query, ("start",))
        startNodes = self.cursor.fetchall() 

        # For each of the start nodes, assemble the trace and write to database
        for startNode in startNodes:
            startNode = self.addColumnNameToData(self.ioevent_cols, startNode)
            startNode["node"] = json.loads(startNode["node"])
            trace = self.getTrace(startNode["node"])
            self.addTraceToDatabase(startNode, trace)
    
    def getTrace(self, node):
        '''
            Given a start node, assemble the system level trace.
        '''
        trace = [node]
        link = self.findLink(node)

        while (link):
            trace.append(link["node"])
            # TODO: Add support for multiple outputs for a single input.
            link = self.findLink(link["node"]["output"][0])

            # If end of trace has been reached, append and return
            if link and link["type"] == "end":
                trace.append(link["node"])
                return trace

        # TODO: If we reached this point, the trace did not end. Add 
        # functionality to deal with this case.
        return trace
        
    def findLink(self, node):
        '''
            Find the linked node.
        '''
        query = 'SELECT * FROM IOEVENTS WHERE ("type" = %s or "type" = %s)\
              and "adli_execution_id" = %s and "adli_execution_index" = %s' 
        self.cursor.execute(query, ("link", "end", node["adliExecutionId"], node["adliExecutionIndex"]))
        row = self.cursor.fetchone() 

        if row:
            rowData = self.addColumnNameToData(self.ioevent_cols, row)
            rowNode = json.loads(rowData["node"])
            if "output" in rowNode:
                # Continue the trace since there is an output for this input.
                return {"type":"link", "node":rowNode}
            else:
                # We've reached the end of the trace.
                return {"type":"end", "node":rowNode}

        return None

    def addTraceToDatabase(self, startNode, traces):
        '''
            Add the trace to the database.
        '''
        if len(traces) == 0:
            print("Trace list is empty. Not adding to database.")
            return 

        traceId = startNode["node"]["uid"]
        systemId = startNode["system_id"]
        version = startNode["system_ver"]
        deploymentId = startNode["deployment_id"]

        version_formatted = version.replace(".","")
        tableName = f"{systemId}_{version_formatted}_traces"

        # Check if the trace uid has already been processed
        query = f'SELECT * FROM {tableName} WHERE trace_id = %s' 
        self.cursor.execute(query, (traceId,))
        hasUid = self.cursor.fetchone()
        if (hasUid is not None):
            print(f"System Trace with UID {traceId} already exists in the database")
            return
        
        # Get the start and end timestamp for this trace
        startTs = traces[0]["timestamp"]
        endTs = None if len(traces) == 1 else traces[-1]["timestamp"]

        startTs = datetime.fromtimestamp(startTs/1000)
        if endTs:
            endTs = datetime.fromtimestamp(endTs/1000)

        # Insert the trace into the database
        sql = f''' INSERT INTO {tableName}(deployment_id, trace_id, start_ts, end_ts, trace_type, traces)
                VALUES(%s,%s,%s,%s,%s,%s) '''
        self.cursor.execute(sql, (deploymentId, traceId, startTs, endTs, None, json.dumps(traces)))
        self.conn.commit()
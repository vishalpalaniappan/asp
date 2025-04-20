import sqlite3
import json
import os

class TraceAssembler:
    '''
        This class is used to process the nodes in the ioEvents.db.
        For every start node, the system level trace is assembled.
        The assembled system level traces are written to the asp.db 
        database in the traces table for the given system.    
    '''

    def __init__(self):
        '''
            Initialize the database connections.
        '''
        path = os.path.dirname(os.path.dirname(__file__))
        sysIoPath = os.path.join(path, "ioEvents.db")
        try:
            self.sysIoConn = sqlite3.connect(sysIoPath)
            self.sysIoCursor = self.sysIoConn.cursor()
            self.ioevent_cols = self.getColumns("IOEVENTS")
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise


        path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        aspPath = os.path.join(path, "asp.db")
        try:
            self.aspConn = sqlite3.connect(aspPath)
            self.aspCursor = self.aspConn.cursor()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise

        self.processDatabase()


    def __del__(self):
        '''
            Clean up database connections.
        '''
        if hasattr(self, 'sysIoConn'):
            self.sysIoConn.close()
        if hasattr(self, 'aspConn'):
            self.aspConn.close()


    def getColumns(self, tableName):
        '''
            Get the columns for a table.
        '''
        query = f'PRAGMA table_info("{tableName}")' 
        self.sysIoCursor.execute(query)
        return self.sysIoCursor.fetchall()
    
    def addColumnNameToData(self, columns, data):
        '''
            Given the column names and the data, create 
            an object which uses the column names as key.
        '''
        obj = {}
        for index, columnValue in enumerate(data):
            obj[columns[index][1]] = columnValue

        return obj


    def processDatabase(self):
        '''
            Processes the database and extracts all the traces.
        '''
        # Get all the start nodes
        query = f'SELECT * FROM "IOEVENTS" WHERE "type" = ?' 
        self.sysIoCursor.execute(query, ["start"])
        startNodes = self.sysIoCursor.fetchall() 

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
            link = self.findLink(link["node"])

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
        query = f'SELECT * FROM "IOEVENTS" WHERE ("type" = ? or "type" = ?)\
              and "adli_execution_id" = ? and "adli_execution_index" = ?' 
        self.sysIoCursor.execute(query, ["link", "end", node["adliExecutionId"], node["adliExecutionIndex"]])
        rows = self.sysIoCursor.fetchall() 

        for row in rows:
            rowData = self.addColumnNameToData(self.ioevent_cols, row)
            rowNode = json.loads(rowData["node"])
            if "output" in rowNode:
                # Continue the trace since there is an output for this input.
                return {"type":"link", "node":rowNode["output"][0]}
            else:
                # We've reached the end of the trace.
                return {"type":"end", "node":rowNode}

        return None
    

    def printTrace(self, startNode, traces):
        '''
            Prints the given trace.
        '''
        print("")
        print(f"Trace ID: {startNode['node']['uid']}")
        for node in traces:
            print(node["fileName"])

    def addTraceToDatabase(self, startNode, traces):
        '''
            Add the trace to the database.
        '''
        if len(traces) == 0:
            print("Trace list is empty. Not adding to database.")
            return 

        traceId = startNode["node"]["uid"]
        systemId = startNode["system_id"]
        version = startNode["sys_ver"]
        deploymentId = startNode["deployment_id"]
        tableName = f"{systemId}_{version}_traces"

        # Check if the trace uid has already been processed
        query = f'SELECT * FROM "{tableName}" WHERE "trace_id" = ?' 
        self.aspCursor.execute(query, [traceId])
        hasUid = self.aspCursor.fetchone()
        if (hasUid is not None):
            print(f"System Trace with UID {traceId} already exists in the database")
            return
        
        # Get the start and end timestamp for this trace
        startTs = traces[0]["timestamp"]
        endTs = traces[0]["timestamp"] if len(traces) == 1 else traces[-1]["timestamp"]

        # Insert the trace into the database
        sql = f''' INSERT INTO "{tableName}"(deployment_id, trace_id, startTs, endTs, traceType, traces)
                VALUES(?,?,?,?,?,?) '''
        self.aspCursor.execute(sql, [deploymentId, traceId, startTs, endTs, None, json.dumps(traces)])
        self.aspConn.commit()

if __name__ == "__main__":
    TraceAssembler()
    
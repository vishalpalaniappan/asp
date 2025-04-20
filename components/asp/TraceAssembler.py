import sqlite3
import json

class TraceAssembler:
    '''
        This class is used to process the nodes in the ioEvents.db.
        For every start node, the system level trace is assembled.
        The assembled system level traces are written to the asp.db 
        database in the traces table for the given system.    
    '''

    def __init__(self, sysIoPath="ioEvents.db", aspPath="asp.db"):
        '''
            Initialize the database connections.
        '''
        try:
            self.sysIoConn = sqlite3.connect(sysIoPath, check_same_thread=False)
            self.sysIoCursor = self.sysIoConn.cursor()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise

        try:
            self.aspConn = sqlite3.connect(aspPath, check_same_thread=False)
            self.aspCursor = self.aspConn.cursor()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise

        self.processDatabase()


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
        # Get the columns
        query = f'PRAGMA table_info("IOEVENTS")' 
        self.sysIoCursor.execute(query)
        columns = self.sysIoCursor.fetchall() 

        # Get all the start nodes
        query = f'SELECT * FROM "IOEVENTS" WHERE "type" = ?' 
        self.sysIoCursor.execute(query, ["start"])
        startNodes = self.sysIoCursor.fetchall() 

        # For each of the start nodes, assemble the trace and write to database
        for startNode in startNodes:
            startNode = self.addColumnNameToData(columns, startNode)
            startNode["node"] = json.loads(startNode["node"])
            trace = self.getTrace(startNode["node"])
            self.addTraceToDatabase(startNode, trace)
            self.printTrace(startNode, trace)
    
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
            node = json.loads(row[8])
            if "output" in node:
                # Continue the trace since there is an output for this input.
                return {"type":"link", "node":node["output"][0]}
            else:
                # We've reached the end of the trace.
                return {"type":"end", "node":node}

        return None
    

    def printTrace(self, startNode, traces):
        '''
            Prints the given trace.
        '''
        print("")
        for node in traces:
            print(node["fileName"], node["funcName"])

    def addTraceToDatabase(self, startNode, traces):
        '''
            Add the trace to the database.
        '''
        traceId = startNode["node"]["uid"]
        systemId = startNode["system_id"]
        version = startNode["sys_ver"]
        deploymentId = startNode["deployment_id"]
        startTs = startNode["ts"]

        tableName = f"{systemId}_{version}_traces"

        # Check if the trace uid has already been processed
        query = f'SELECT * FROM "{tableName}" WHERE "trace_id" = ?' 
        self.aspCursor.execute(query, [traceId])
        hasUid = self.aspCursor.fetchone()
        if (hasUid is not None):
            print(f"System Trace with UID {traceId} already exists in the database")
            return

        # Insert the trace into the database
        sql = f''' INSERT INTO "{tableName}"(deployment_id, trace_id, startTs, endTs, traceType, traces)
                VALUES(?,?,?,?,?,?) '''
        self.aspCursor.execute(sql, [deploymentId, traceId, startTs, 0.0, "1", json.dumps(traces)])
        self.aspConn.commit()

if __name__ == "__main__":
    TraceAssembler()
    
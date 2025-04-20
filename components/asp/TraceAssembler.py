import sqlite3
import json

class TraceAssembler:

    def __init__(self, sysIoPath="ioEvents.db", aspPath="asp.db"):
        '''
            Initialize the database connection.
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
        obj = {}
        for index, columnValue in enumerate(data):
            obj[columns[index][1]] = columnValue

        return obj


    def processDatabase(self):
        '''
            Processes the database and extracts all the traces.
        '''
        query = f'PRAGMA table_info("IOEVENTS")' 
        self.sysIoCursor.execute(query)
        columns = self.sysIoCursor.fetchall() 

        query = f'SELECT * FROM "IOEVENTS" WHERE "type" = ?' 
        self.sysIoCursor.execute(query, ["start"])
        startNodes = self.sysIoCursor.fetchall() 

        for startNode in startNodes:
            parsedStartNode = self.addColumnNameToData(columns, startNode)
            parsedStartNode["node"] = json.loads(parsedStartNode["node"])
            trace = self.getTrace(parsedStartNode["node"])
            self.addNodeToDatabase(parsedStartNode, trace)
    
    def getTrace(self, node):
        '''
            Given a node get the system level trace.
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

        # Trace did not end
        return trace
        
    def findLink(self, node):
        '''
            Find the link given a node.
        '''
        query = f'SELECT * FROM "IOEVENTS" WHERE ("type" = ? or "type" = ?) and "adli_execution_id" = ? and "adli_execution_index" = ?' 
        self.sysIoCursor.execute(query, ["link", "end", node["adliExecutionId"], node["adliExecutionIndex"]])
        rows = self.sysIoCursor.fetchall() 

        for row in rows:
            node = json.loads(row[8])
            if "output" in node:
                return {"type":"link", "node":node["output"][0]}
            else:
                return {"type":"end", "node":node}

        return None
    

    def printTrace(self, startNode, trace):
        print("")
        print(startNode)
        for node in trace:
            print(node["fileName"])

    def addNodeToDatabase(self, startNode, traces):
        traceId = startNode["node"]["uid"]
        systemId = startNode["system_id"]
        version = startNode["sys_ver"]
        deploymentId = startNode["deployment_id"]
        startTs = startNode["ts"]

        tableName = f"{systemId}_{version}_traces"
        query = f'SELECT * FROM "{tableName}" WHERE "trace_id" = ?' 
        self.aspCursor.execute(query, [traceId])
        hasUid = self.aspCursor.fetchone()

        if (hasUid is not None):
            print(f"System Trace with UID {traceId} already exists in the database")
            return

        sql = f''' INSERT INTO "{tableName}"(deployment_id, trace_id, startTs, endTs, traceType, traces)
                VALUES(?,?,?,?,?,?) '''
        self.aspCursor.execute(sql, [deploymentId, traceId, startTs, 0.0, "1", json.dumps(traces)])
        self.aspConn.commit()

if __name__ == "__main__":
    TraceAssembler()
    
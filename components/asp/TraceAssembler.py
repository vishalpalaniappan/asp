import sqlite3
import json

class TraceAssembler:

    def __init__(self, db_path="ioEvents.db"):
        try:
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise

        self.getStartNodes()

    def getStartNodes(self):

        query = f'PRAGMA table_info("IOEVENTS")' 
        self.cursor.execute(query)
        rows = self.cursor.fetchall() 

        query = f'SELECT * FROM "IOEVENTS" WHERE "type" = ?' 
        self.cursor.execute(query, ["start"])
        nodes = self.cursor.fetchall() 

        startNodes = []
        for node in nodes:
            startNodes.append({
                "executionId": node[5],
                "executionIndex": node[6],
                "node": json.loads(node[8])
            })

            trace = self.getTrace(startNodes[-1]["node"])
            self.addNodeToDatabase(trace)

        return startNodes
    
    def getTrace(self, node):
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
        query = f'SELECT * FROM "IOEVENTS" WHERE ("type" = ? or "type" = ?) and "adli_execution_id" = ? and "adli_execution_index" = ?' 
        self.cursor.execute(query, ["link", "end", node["adliExecutionId"], node["adliExecutionIndex"]])
        rows = self.cursor.fetchall() 

        for row in rows:
            node = json.loads(row[8])
            if "output" in node:
                return {"type":"link", "node":node["output"][0]}
            else:
                return {"type":"end", "node":node}

        return None
    

    def addNodeToDatabase(self, trace):
        print(len(trace))

if __name__ == "__main__":
    TraceAssembler()
    
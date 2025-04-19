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
        rows = self.cursor.fetchall() 

        startNodes = []
        for row in rows:
            startNodes.append({
                "executionId": row[5],
                "executionIndex": row[6],
                "node": row[8]
            })

        return startNodes



if __name__ == "__main__":
    TraceAssembler()
    
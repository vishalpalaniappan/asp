import time
import mysql.connector
import sys
import json
from DbConn import DBClient

class IOEventsTest:

    def __init__(self):
        with DBClient() as db:
            self.conn = db.conn
            self.cursor = db.cursor

if __name__ == "__main__":
    a = IOEventsTest()
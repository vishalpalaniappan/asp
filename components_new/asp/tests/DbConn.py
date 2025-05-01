import mysql.connector
import os 

def get_connection():
    
    isDocker = os.environ.get('IS_RUNNING_IN_DOCKER', False)

    if isDocker:
        host = "mariadb-container"
    else:
        host = "localhost"

    return mysql.connector.connect(
        host= host,
        user= "root",
        password= "random-password",
        database= "aspDatabase",
        port= "3306"
    )

class DBClient:
    def __enter__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()
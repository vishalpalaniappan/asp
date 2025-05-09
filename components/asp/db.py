import mysql.connector
import os 
import time

def get_connection():
    
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
                port= "3306"
            )
        except Exception as e:
            print(f"Attempt {attempt + 1}: {e}")
            print("Trying again in 5 seconds.")
            attempt += 1
        time.sleep(5)

    raise Exception(f"Tried to connect to database {attempt} times but failed.")

class DBClient:
    """
    A context manager for database operations.
    
    Handles connection creation and cleanup automatically when used in a with statement.
    Example:
        with DBClient() as db:
            db.cursor.execute("SELECT * FROM table")
            results = db.cursor.fetchall()
    """
    def __enter__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            if exc_type is None:
                # Commit if no exception occurred
                self.conn.commit()
            self.conn.close()
        
        # Return False to propagate exceptions
        return False
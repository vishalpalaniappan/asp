import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="random-password",
        database="aspDatabase",
        port="3306"
    )

class DBClient:
    def __enter__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()
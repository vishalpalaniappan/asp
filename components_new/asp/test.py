import time
import mysql.connector
import sys

time.sleep(5)

global cursor, conn, count
count = 0

def writeToDatabase():
    while True:
        time.sleep(10)
        global count, cursor, conn
        count += 1

        insert_query = """
        INSERT INTO data9 (name, email)
        VALUES (%s, %s)
        """

        values = (str(count), str(count))
        cursor.execute(insert_query, values)
        conn.commit()

def main(argv):
    try:
        global cursor, conn, count
        conn = mysql.connector.connect(
            host="mariadb-container",
            user="root",
            password="random-password",
            database="asp-database",
            port="3306"
        )

        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        print(cursor.fetchone())

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS data9 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
    except Exception as e:
        print("EXCEPTION:", e)
        return -1

    writeToDatabase()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
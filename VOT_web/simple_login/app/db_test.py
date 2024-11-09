import mysql.connector
import os

def test_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "db"),
            user=os.getenv("DB_USER", "user"),
            password=os.getenv("DB_PASSWORD", "user_password"),
            database=os.getenv("DB_NAME", "login_db"),
            port=int(os.getenv("DB_PORT", 3306))
        )
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        print("Connected to database:", cursor.fetchone())
    except mysql.connector.Error as err:
        print("Database connection error:", err)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    test_db_connection()

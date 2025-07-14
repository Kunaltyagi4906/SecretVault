import os
import sqlite3
import mysql.connector

print("🔁 USE_SQLITE =", os.environ.get("USE_SQLITE"))

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Path of current `db.py` file
DB_PATH = os.path.join(BASE_DIR, '..', 'database.db')  # Go 1 level up and locate `database.db`

def get_db_connection():
    use_sqlite = os.environ.get("USE_SQLITE", "false").lower() == "true"

    if use_sqlite:
        print(f"🔗 Connecting to SQLite at: {DB_PATH}")
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    else:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="myvault_backend"
        )

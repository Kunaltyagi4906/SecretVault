import os
import sqlite3
import mysql.connector

# 🔗 Construct absolute path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'database.db'))

print("🔗 Connecting to SQLite at:", DB_PATH)

def get_db_connection():
    use_sqlite = os.environ.get("USE_SQLITE", "false").lower() == "true"

    if use_sqlite:
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

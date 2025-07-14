import os
import sqlite3
import mysql.connector
print("🔁 USE_SQLITE =", os.environ.get("USE_SQLITE"))

def get_db_connection():
    use_sqlite = os.environ.get("USE_SQLITE", "false").lower() == "true"

    if use_sqlite:
        conn = sqlite3.connect("database.db")
        conn.row_factory = sqlite3.Row
        return conn
    else:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root123",
            database="myvault_backend"
        )

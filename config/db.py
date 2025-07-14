import os
import sqlite3
import mysql.connector

def get_db_connection():
    use_sqlite = os.environ.get("USE_SQLITE", "False").lower() == "True"

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

import os
import sqlite3
import mysql.connector

# TEMPORARY FIX
print("🔁 USE_SQLITE =", os.environ.get("USE_SQLITE"))

use_sqlite = os.environ.get("USE_SQLITE", "false").lower() == "true"
# Hugging Face environment check
if "SPACE_ID" in os.environ:
    print("📦 Running on Hugging Face Space — forcing SQLite")
    use_sqlite = True

def get_db_connection():
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

import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",     # 🔑 update if your password is different
        database="myvault_backend"
    )

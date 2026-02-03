import sqlite3
from sqlite3 import Connection



DB_NAME = "vanghee_gst.db"

def get_connection() -> Connection:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # fetch results as dict
    return conn
def get_connection():
    return sqlite3.connect("vanghee.db")
def init_db():
    from database.models import create_tables

    conn = get_connection()
    create_tables(conn)
    conn.commit()
    conn.close()
    print("Database initialized ✅")

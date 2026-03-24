import csv
from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20) NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


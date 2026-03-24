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


def insert_from_csv(file_path):
    conn = get_connection()
    cur = conn.cursor()

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                cur.execute(
                    "INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING",
                    (row['name'], row['phone'])
                )
            except Exception as e:
                print("Error inserting row:", row, e)

    conn.commit()
    cur.close()
    conn.close()


def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


def update_contact():
    name = input("Enter existing name: ")
    new_name = input("Enter new name (leave blank to skip): ")
    new_phone = input("Enter new phone (leave blank to skip): ")

    conn = get_connection()
    cur = conn.cursor()

    if new_name:
        cur.execute("UPDATE phonebook SET name=%s WHERE name=%s", (new_name, name))

    if new_phone:
        cur.execute("UPDATE phonebook SET phone=%s WHERE name=%s", (new_phone, name))

    conn.commit()
    cur.close()
    conn.close()

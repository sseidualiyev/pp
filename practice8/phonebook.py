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



def query_contacts():
    print("1 - All contacts")
    print("2 - Search by name")
    print("3 - Search by phone prefix")

    choice = input("Choose option: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        cur.execute("SELECT * FROM phonebook")

    elif choice == "2":
        name = input("Enter name: ")
        cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s", ('%' + name + '%',))

    elif choice == "3":
        prefix = input("Enter phone prefix: ")
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (prefix + '%',))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def delete_contact():
    print("1 - Delete by name")
    print("2 - Delete by phone")

    choice = input("Choose option: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")
        cur.execute("DELETE FROM phonebook WHERE name=%s", (name,))

    elif choice == "2":
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))

    conn.commit()
    cur.close()
    conn.close()



def main():
    create_table()

    while True:
        print("\nPhoneBook Menu:")
        print("1 - Insert from CSV")
        print("2 - Insert from console")
        print("3 - Update contact")
        print("4 - Query contacts")
        print("5 - Delete contact")
        print("0 - Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_from_csv("contacts.csv")
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

def search_pattern():
    pattern = input("Enter search pattern: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    
    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()

def insert_or_update():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))

    conn.commit()
    cur.close()
    conn.close()

def insert_many():
    names = ["Ali", "John", "Test"]
    phones = ["777123456", "abc123", "999888777"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL insert_many_users(%s, %s, %s)", (names, phones, None))

    conn.commit()
    cur.close()
    conn.close()

def pagination():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()

def delete_user():
    value = input("Enter name or phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_user(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()
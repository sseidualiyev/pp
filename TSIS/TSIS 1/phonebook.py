import json
import csv
from connect import get_connection


# =========================
# BASIC HELPERS
# =========================

def get_group_id(cur, group_name):
    cur.execute("""
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """, (group_name,))

    cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
    return cur.fetchone()[0]


def get_contact_id(cur, name):
    cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
    res = cur.fetchone()
    return res[0] if res else None


# =========================
# ADD CONTACT
# =========================

def add_contact(conn):
    cur = conn.cursor()

    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")

    gid = get_group_id(cur, group)

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (name, email, birthday, gid))

    cid = cur.fetchone()[0]

    while True:
        phone = input("Phone (or empty to stop): ")
        if not phone:
            break
        ptype = input("Type (home/work/mobile): ")

        cur.execute("""
            INSERT INTO phones(contact_id, phone, type)
            VALUES (%s, %s, %s)
        """, (cid, phone, ptype))

    conn.commit()
    print("✅ Contact added.")



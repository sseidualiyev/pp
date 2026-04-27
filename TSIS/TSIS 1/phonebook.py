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



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


# =========================
# FILTER + SORT
# =========================

def view_contacts(conn):
    cur = conn.cursor()

    group = input("Filter by group (or Enter): ")
    sort = input("Sort by (name/birthday/date): ")

    query = """
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """

    params = []

    if group:
        query += " WHERE g.name = %s"
        params.append(group)

    if sort == "birthday":
        query += " ORDER BY c.birthday"
    elif sort == "date":
        query += " ORDER BY c.id"
    else:
        query += " ORDER BY c.name"

    cur.execute(query, params)

    for row in cur.fetchall():
        print(row)



# =========================
# SEARCH
# =========================

def search(conn):
    cur = conn.cursor()
    q = input("Search query: ")

    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    for row in cur.fetchall():
        print(row)


# =========================
# PAGINATION
# =========================

def paginate(conn):
    cur = conn.cursor()
    limit = 5
    offset = 0

    while True:
        cur.execute("""
            SELECT c.name, c.email
            FROM contacts c
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        if not rows:
            print("No more data.")
            break

        for r in rows:
            print(r)

        cmd = input("next / prev / quit: ").lower()

        if cmd == "next":
            offset += limit
        elif cmd == "prev" and offset >= limit:
            offset -= limit
        elif cmd == "quit":
            break


# =========================
# EXPORT JSON
# =========================

def export_json(conn):
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """)

    data = []

    for row in cur.fetchall():
        cid = row[0]

        cur.execute("SELECT phone, type FROM phones WHERE contact_id=%s", (cid,))
        phones = cur.fetchall()

        data.append({
            "name": row[1],
            "email": row[2],
            "birthday": str(row[3]),
            "group": row[4],
            "phones": [{"number": p[0], "type": p[1]} for p in phones]
        })

    with open("contacts.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Exported to contacts.json")


# =========================
# IMPORT JSON
# =========================

def import_json(conn):
    cur = conn.cursor()

    with open("contacts.json") as f:
        data = json.load(f)

    for contact in data:
        name = contact["name"]

        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists (skip/overwrite): ")

            if choice == "skip":
                continue
            elif choice == "overwrite":
                cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        cur.execute("""
            INSERT INTO contacts(name, email, birthday)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (name, contact["email"], contact["birthday"]))

        cid = cur.fetchone()[0]

        gid = get_group_id(cur, contact["group"])

        cur.execute("UPDATE contacts SET group_id=%s WHERE id=%s", (gid, cid))

        for p in contact["phones"]:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (cid, p["number"], p["type"]))

    conn.commit()
    print("✅ JSON imported.")


# =========================
# IMPORT CSV
# =========================

def import_csv(conn):
    cur = conn.cursor()

    filename = input("CSV filename: ")

    with open(filename) as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = row["name"]

            cur.execute("""
                INSERT INTO contacts(name, email, birthday)
                VALUES (%s, %s, %s)
                ON CONFLICT DO NOTHING
                RETURNING id
            """, (name, row["email"], row["birthday"]))

            res = cur.fetchone()

            if res:
                cid = res[0]
            else:
                cid = get_contact_id(cur, name)

            gid = get_group_id(cur, row["group"])

            cur.execute("UPDATE contacts SET group_id=%s WHERE id=%s", (gid, cid))

            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (cid, row["phone"], row["type"]))

    conn.commit()
    print("✅ CSV imported.")



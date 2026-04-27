import psycopg2
import json
import csv

def connect():
    return psycopg2.connect(
        dbname="phonebook_db",
        user="postgres",
        password="Sagi2008",
        host="localhost",
        port="5432"
    )
def search_contacts(conn, query="", group=None, sort_by="name"):
    cur = conn.cursor()

    sql = """
    SELECT c.name, c.email, c.birthday, g.name
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    WHERE (c.name ILIKE %s OR c.email ILIKE %s)
    """

    params = [f"%{query}%", f"%{query}%"]

    if group:
        sql += " AND g.name = %s"
        params.append(group)

    if sort_by == "name":
        sql += " ORDER BY c.name"
    elif sort_by == "birthday":
        sql += " ORDER BY c.birthday"

    cur.execute(sql, params)
    return cur.fetchall()
def paginate(data, page=1, per_page=5):
    start = (page - 1) * per_page
    end = start + per_page
    return data[start:end]


def console_navigation(data):
    page = 1

    while True:
        page_data = paginate(data, page)

        for row in page_data:
            print(row)

        cmd = input("next / prev / quit: ")

        if cmd == "next":
            page += 1
        elif cmd == "prev" and page > 1:
            page -= 1
        elif cmd == "quit":
            break

def export_json(conn):
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """)

    data = cur.fetchall()

    result = []

    for r in data:
        result.append({
            "name": r[0],
            "email": r[1],
            "birthday": str(r[2]),
            "group": r[3]
        })

    with open("contacts.json", "w") as f:
        json.dump(result, f, indent=4)

def import_json(conn):
    cur = conn.cursor()

    with open("contacts.json") as f:
        data = json.load(f)

    for c in data:
        cur.execute("SELECT id FROM contacts WHERE name=%s", (c["name"],))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{c['name']} exists (skip/overwrite): ")

            if choice == "skip":
                continue
            elif choice == "overwrite":
                cur.execute("DELETE FROM contacts WHERE name=%s", (c["name"],))

        cur.execute("""
            INSERT INTO contacts(name, email, birthday)
            VALUES (%s, %s, %s)
        """, (c["name"], c["email"], c["birthday"]))

    conn.commit()

def import_csv(conn):
    cur = conn.cursor()

    with open("contacts.csv") as f:
        reader = csv.DictReader(f)

        for row in reader:
            cur.execute("""
                INSERT INTO contacts(name, email, birthday)
                VALUES (%s, %s, %s)
            """, (row["name"], row["email"], row["birthday"]))

    conn.commit()

def main():
    conn = connect()

    while True:
        print("\n1.Search 2.Export JSON 3.Import JSON 4.Import CSV 5.Exit")
        choice = input("Choose: ")

        if choice == "1":
            q = input("Search: ")
            data = search_contacts(conn, q)
            console_navigation(data)

        elif choice == "2":
            export_json(conn)

        elif choice == "3":
            import_json(conn)

        elif choice == "4":
            import_csv(conn)

        elif choice == "5":
            break

    conn.close()

if __name__ == "__main__":
    main()
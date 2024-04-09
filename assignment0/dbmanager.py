import sqlite3

def createdb(db_name):
    '''Creates an sqlite3 database (if not created) and makes a connection to the db'''
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    try:
        cur.execute("""CREATE TABLE incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
                )""")
        # print('CREATED THE DATABASE {}'.format(db_name))
    except Exception as e:
        if "table incidents already exists" in str(e):
            print("Table already exists. No need to create.")
        else:
            # Handle other OperationalError cases
            print(f"Error: {e}")
    con.commit()
    cur.close()
    return con

def populatedb(con, incidents):
    '''Inserts incident data into the database'''
    cur = con.cursor()
    sqlite_insert_query = """INSERT INTO incidents
                          (incident_time, incident_number, incident_location, nature, incident_ori) 
                          VALUES (?, ?, ?, ?, ?);"""
    cur.executemany(sqlite_insert_query, incidents)
    # print('ADDED DATA IN SQLITE3 DATABASE!')
    # print('rows affected = ', cur.rowcount)
    cur.execute("SELECT COUNT(*) FROM incidents")
    total_rows = cur.fetchone()[0]
    # print('Total Number of rows in the table = ', total_rows)
    con.commit()
    cur.close()

def status(con):
    """
    Prints a list of the nature of incidents and the number of times they have occurred.
    """
    cur = con.cursor()
    cur.execute("""
        SELECT nature, COUNT(*) AS incident_count
        FROM incidents
        GROUP BY nature
        ORDER BY incident_count DESC, nature
    """)
    rows = cur.fetchall()
    empty_natures = list()
    for row in rows:
        nature, incident_count = row
        if nature=='':
            empty_natures.append((nature, incident_count))
            continue
        print(f"{nature}|{incident_count}")
    for row in empty_natures:
        nature, incident_count = row
        print(f"{nature}|{incident_count}")
    cur.close()
    con.close()

    

if __name__ == "__main__":
    con = createdb('resources/sample.db')
    incidents_data = [
        ("2022-01-01 12:30", "2022-000001", "123eAFA Main St", "Suspicious", "OK123456"),
        ("2022 qw4G", " 2arsdGTQ", "qefQR", "Gunshots", "qeEAFr")
        # Add more incident data as needed
    ]
    populatedb(con, incidents_data)
    status(con)
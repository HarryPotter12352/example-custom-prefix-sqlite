import sqlite3



def init_prefix_db():
    conn = sqlite3.connect("prefix.db")
    c = conn.cursor()
    with conn:
        try:
            c.execute("""CREATE TABLE prefix_data (
                id integer,
                prefix string
            )""")
        except:
            print("Database and table already exists, creation job terminated")
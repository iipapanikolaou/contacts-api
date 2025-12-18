import sqlite3

DATABASE_FILENAME = 'contacts.db'

def init_db():
    conn = sqlite3.connect(DATABASE_FILENAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            number TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        );
    """)
    conn.commit()

    cursor.close()
    conn.close()

    new_conn = sqlite3.connect("contacts.db")
    new_cursor = new_conn.cursor()
    rows = new_cursor.execute("SELECT name FROM sqlite_master")

    return rows.fetchone() is None


def get_contact_by_id(contact_id):

    conn = sqlite3.connect(DATABASE_FILENAME)
    cursor = conn.cursor()

    rows = cursor.execute('SELECT id,name,number FROM contacts WHERE id = ?', contact_id)
    
    return rows.fetchone()

def create_contact(name, number):

    conn = sqlite3.connect(DATABASE_FILENAME)
    cursor = conn.cursor()

    cursor.execute('INSERT INTO contacts (name,number) VALUES(?,?)',(name,number,))
    conn.commit()

    if cursor.lastrowid:
        rows = cursor.execute('SELECT id,name,number FROM contacts WHERE id = ?')
        return rows.fetchone()
    
    return None


    return cursor.lastrowid

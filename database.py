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

    new_conn = sqlite3.connect(DATABASE_FILENAME)
    new_cursor = new_conn.cursor()
    rows = new_cursor.execute("SELECT name FROM sqlite_master")

    return not rows.fetchone() is None


def get_contacts(page,limit):

    conn = sqlite3.connect(DATABASE_FILENAME)
    cursor = conn.cursor()

    start_id = (page - 1)* limit + 1
    end_id = start_id + limit - 1 

    cursor.execute('SELECT id,name,number FROM contacts WHERE id >= ? AND id <= ? ',(start_id,end_id,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def count_contacts():

    conn = sqlite3.connect(DATABASE_FILENAME)
    cursor = conn.cursor()

    row = cursor.execute('SELECT COUNT(*) FROM contacts').fetchone()

    cursor.close()
    conn.close()

    return row[0]

def get_contact_by_id(contact_id):

    conn = sqlite3.connect(DATABASE_FILENAME)
    cursor = conn.cursor()

    row = cursor.execute('SELECT id,name,number FROM contacts WHERE id = ?', contact_id).fetchone()

    cursor.close()
    conn.close()
    
    return row

def create_contact(name, number):

    conn = sqlite3.connect(DATABASE_FILENAME)
    cursor = conn.cursor()

    cursor.execute('INSERT INTO contacts (name,number) VALUES(?,?)',(name,number,))
    conn.commit()

    if cursor.lastrowid:
        rows = cursor.execute('SELECT id,name,number FROM contacts WHERE id = ?', (cursor.lastrowid,))
        return rows.fetchone()
    
    return None

def update_contact(contact_id, name, number):

    conn = sqlite3.connect(DATABASE_FILENAME)
    cursor = conn.cursor()

    try:
        cursor.execute('UPDATE contacts SET name = ?, number = ? WHERE id = ?',(name, number, contact_id,))
        conn.commit()
    except sqlite3.Error:
        cursor.close()
        conn.close()
        return None
    
    row = get_contact_by_id(contact_id)
    cursor.close()
    conn.close()
    return row
    
def delete_contact(contact_id):

    conn = sqlite3.connect(DATABASE_FILENAME)
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM contacts WHERE id = ?',(contact_id,))
        conn.commit()
    except sqlite3.Error:
        cursor.close()
        conn.close()
        return False
    
    cursor.close()
    conn.close()
    return True
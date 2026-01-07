import sqlite3

DATABASE_FILENAME = 'contacts.db'

FILTERS = {'search': 'name LIKE ?',
           'number': 'number = ?'}

def init_db():

    with sqlite3.connect(DATABASE_FILENAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                number TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                deleted_at DEFAULT NULL
            );
        """)
        conn.commit()

def get_contacts(page:int,limit:int,arguments:list):

    placeholder_values = []

    where_clause = create_where_clause(arguments,placeholder_values)

    sql_query = """
    SELECT id, name, number 
    FROM contacts
    """ + where_clause + """
    ORDER BY id ASC
    LIMIT ?
    OFFSET ?
    """

    offset_rows = (page - 1) * limit

    placeholder_values.append(limit)
    placeholder_values.append(offset_rows)

    placeholder_values_tuple = tuple(placeholder_values)

    with sqlite3.connect(DATABASE_FILENAME) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_query,placeholder_values_tuple)
        rows = cursor.fetchall()

    contacts = map_rows_to_contacts(rows)

    return contacts

def count_contacts(arguments:list):

    placeholder_values = []

    where_clause = create_where_clause(arguments,placeholder_values)

    sql_query = """
    SELECT COUNT(*) 
    FROM contacts 
    """ + where_clause

    placeholder_values_tuple = tuple(placeholder_values)

    with sqlite3.connect(DATABASE_FILENAME) as conn:
        cursor = conn.cursor()
        row = cursor.execute(sql_query,placeholder_values_tuple).fetchone()

        total_contacts = row[0]

    return total_contacts

def get_contact_by_id(contact_id):

    with sqlite3.connect(DATABASE_FILENAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id,name,number FROM contacts WHERE id = ? AND deleted_at IS NULL', (contact_id,))
        row = cursor.fetchone()
    
    return map_values_to_contact(row) if row else None

def create_contact(name, number):

    with sqlite3.connect(DATABASE_FILENAME) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO contacts (name, number) VALUES(?,?)',(name,number,))
        conn.commit()
    
    return cursor.lastrowid

def update_contact(contact_id, name, number):

    with sqlite3.connect(DATABASE_FILENAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE contacts SET name = ?, number = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?',(name, number, contact_id,))
        conn.commit()
    
    return cursor.rowcount > 0
    
def remove_contact(contact_id):

    with sqlite3.connect(DATABASE_FILENAME) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE contacts SET updated_at = CURRENT_TIMESTAMP, deleted_at = CURRENT_TIMESTAMP WHERE id = ?',(contact_id,))
        conn.commit()

    affected_rows = cursor.rowcount
    
    return affected_rows

def map_values_to_contact(row):

    if not row:
        return None

    contact = {
        'id' : int(row[0]),
        'name' : row[1],
        'number' : row[2]
    }

    return contact

def map_rows_to_contacts(rows):

    if not rows:
        return []

    contacts = []

    for row in rows:
        contact = map_values_to_contact(row)
        contacts.append(contact)

    return contacts

def create_where_clause(arguments:list, placeholder_values:list) -> tuple[str,list]:
    args = {
        key:value for key,value in arguments.items()
        if key not in ['page','limit']
    }

    conditional_clauses = ['deleted_at IS NULL']

    if 'search' in args:
        conditional_clauses.append(FILTERS['search'])
        placeholder_values.append(f'%{args.get("search","")}%')
        del args['search']

    for key in args.keys():
        if key in FILTERS.keys():
            conditional_clauses.append(FILTERS[key])
            placeholder_values.append(args[key])

    where_clause = 'WHERE ' + ' AND '.join(conditional_clauses) + ' ' if conditional_clauses else ''

    return where_clause
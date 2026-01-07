import sqlite3

DATABASE_FILENAME = 'contacts.db'

def init_db():

    with sqlite3.connect(DATABASE_FILENAME) as conn:
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

def get_contacts(page,limit,arguments):

    offset_rows = (page - 1) * limit

    search_arg = arguments.get('search','%%')

    where_clause = 'WHERE name LIKE ? '

    query_placeholder_values = [search_arg]

    args = arguments.copy()
    try:
        del args['search']
    except KeyError:
        pass
    try:
        del args['page']
    except KeyError:
        pass
    try:
        del args['limit']
    except KeyError:
        pass

    for key,value in args.items():
        where_clause += f'AND {key} = ? '
        query_placeholder_values.append(value)

    sql_query = """
    SELECT id, name, number 
    FROM contacts
    """ + where_clause + """
    ORDER BY id ASC
    LIMIT ?
    OFFSET ?
    """

    print(sql_query)

    query_placeholder_values.append(limit)
    query_placeholder_values.append(offset_rows)

    query_params_tuple = tuple(query_placeholder_values)

    with sqlite3.connect(DATABASE_FILENAME) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_query,query_params_tuple)
        rows = cursor.fetchall()

    contacts = map_rows_to_contacts(rows)

    return contacts

def count_contacts(query_arguments:list):

    args = query_arguments.copy()

    where_clause = 'WHERE name LIKE ? '

    name = args.get('search','%%')

    placeholder_values = [name]

    try:
        del args['search']
    except KeyError:
        pass
    try:
        del args['page']
    except KeyError:
        pass
    try:
        del args['limit']
    except KeyError:
        pass

    for key,value in args.items():
        where_clause += f'AND {key} = ? '
        placeholder_values.append(value)

    placeholder_values_tuple = tuple(placeholder_values)

    sql_query = """
    SELECT COUNT(*) 
    FROM contacts 
    """ + where_clause

    with sqlite3.connect(DATABASE_FILENAME) as conn:
        cursor = conn.cursor()
        row = cursor.execute(sql_query,placeholder_values_tuple).fetchone()

        total_contacts = row[0]

    return total_contacts

def get_contact_by_id(contact_id):

    with sqlite3.connect(DATABASE_FILENAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id,name,number FROM contacts WHERE id = ?', (contact_id,))
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
        cursor.execute('DELETE FROM contacts WHERE id = ?',(contact_id,))
        conn.commit()
    
    return cursor.rowcount > 0

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
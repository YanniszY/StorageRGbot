import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS file_id (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        file_type TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

def execute_query(query, params=()):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    result = cursor.fetchall()
    conn.close()
    return result

def insert_file(file_id, file_type):
    execute_query("INSERT INTO file_id (text, file_type) VALUES (?, ?)", (file_id, file_type))

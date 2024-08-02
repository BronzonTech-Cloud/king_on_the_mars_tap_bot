import sqlite3

DB_NAME = 'users.db'

def create_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            taps INTEGER DEFAULT 0,
            address TEXT,
            last_claimed TEXT
        )
    ''')
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return {'user_id': user[1], 'taps': user[2], 'address': user[3], 'last_claimed': user[4]}

def update_taps(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET taps = taps + 1 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def set_user_address(user_id, address):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET address = ? WHERE user_id = ?', (address, user_id))
    conn.commit()
    conn.close()

def set_last_claimed(user_id, timestamp):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET last_claimed = ? WHERE user_id = ?', (timestamp, user_id))
    conn.commit()
    conn.close()

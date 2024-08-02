import sqlite3
from ton import send_ton_tokens

DB_NAME = 'users.db' 

def reward_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, address, taps FROM users WHERE taps > 0')
    users = cursor.fetchall()
    conn.close()
    
    for user in users:
        user_id, address, taps = user
        if address:
            token_amount = taps  # Adjust this logic as needed
            send_ton_tokens(address, token_amount)

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET taps = 0 WHERE user_id = ?', (user_id,))
            conn.commit()
            conn.close()

if __name__ == '__main__':
    reward_users()

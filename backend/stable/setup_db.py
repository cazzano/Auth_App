import sqlite3

# Connect to SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('users.db')

# Create a cursor object
cursor = conn.cursor()

# Create a users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

# Insert a sample user (you can change the username and password)
cursor.execute('''
    INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)
''', ('admin', 'admin1234'))

# Commit changes and close the connection
conn.commit()
conn.close()

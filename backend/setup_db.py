import sqlite3

# Connect to the database
conn = sqlite3.connect('database.db')

# Create a cursor
c = conn.cursor()

# Create the images table with an additional column for predictions
c.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        path TEXT NOT NULL,
        prediction TEXT
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
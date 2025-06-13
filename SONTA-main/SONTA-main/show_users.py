import sqlite3

conn = sqlite3.connect('sonta.db')
c = conn.cursor()
for row in c.execute('SELECT id, username, email FROM users'):
    print(row)
conn.close()
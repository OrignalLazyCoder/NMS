import sqlite3

conn = sqlite3.connect('database')
c = conn.cursor()
out = (c.execute('SELECT * FROM users'))
for i in out:
    print(i)
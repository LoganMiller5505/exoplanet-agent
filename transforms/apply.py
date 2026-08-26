import sqlite3

conn = sqlite3.connect("data/exoplanets.db")
cursor = conn.cursor()

with open("transforms/views/default.sql", "r") as f:
    sql = f.read()
cursor.executescript(sql)

with open("transforms/views/habitable.sql", "r") as f:
    sql = f.read()
cursor.executescript(sql)

conn.commit()
conn.close()

print("Views created successfully.")
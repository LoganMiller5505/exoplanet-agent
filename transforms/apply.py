import sqlite3

conn = sqlite3.connect("data/exoplanets.db")
cursor = conn.cursor()

with open("transforms/views/habitable.sql", "r") as f:
    sql = f.read()

cursor.execute(sql)
conn.commit()

print("Views created successfully.")
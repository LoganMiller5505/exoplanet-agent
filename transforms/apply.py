import sqlite3

conn = sqlite3.connect("data/exoplanets.db")
cursor = conn.cursor()

with open("transforms/views/default.sql", "r") as f:
    sql = f.read()
cursor.executescript(sql)

with open("transforms/views/planets.sql", "r") as f:
    sql = f.read()
cursor.executescript(sql)

with open("transforms/views/planet_names.sql", "r") as f:
    sql = f.read()
cursor.executescript(sql)

with open("transforms/views/candidates.sql", "r") as f:
    sql = f.read()
cursor.executescript(sql)

with open("transforms/views/habitable_zone.sql", "r") as f:
    sql = f.read()
cursor.executescript(sql)

with open("transforms/views/planet_classes.sql", "r") as f:
    sql = f.read()
cursor.executescript(sql)

with open("transforms/views/systems.sql", "r") as f:
    sql = f.read()
cursor.executescript(sql)

conn.commit()
conn.close()

print("Views created successfully.")
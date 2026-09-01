import os

import psycopg
from dotenv import load_dotenv

load_dotenv()
conn_string = os.getenv("DATABASE_URL")

with psycopg.connect(conn_string) as conn:
    print("Connected to the database successfully.")
    with conn.cursor() as cur:
        # Dependency order, not alphabetical: staging builds stg_ps and stg_k2pandc,
        # which planets reads; habitable_zone, planet_classes and systems all read
        # stg_planets, so planets must come before them.
        for name in ["staging", "planets", "planet_names", "candidates",
                     "habitable_zone", "planet_classes", "systems"]:
            with open(f"transforms/views/{name}.sql", "r") as f:
                cur.execute(f.read())
            print(f"Applied {name}.sql successfully.")
import os

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()
conn_string = os.getenv("DATABASE_URL")

class QueryError(Exception):
    pass

DB_PATH = "data/exoplanets.db"

conn = None

def connect():
    # autocommit is required now that the connection is reused: without it the first
    # SELECT opens a transaction that is never closed, leaving the connection sitting
    # 'idle in transaction' for the life of the process. Closing per query used to roll
    # that back implicitly. Every query here is read-only, so there is nothing to commit.
    return psycopg.connect(conn_string, row_factory=dict_row, autocommit=True)

def query(sql, limit=50):
    global conn
    if conn is None:
        conn = connect()
        print("Initial connection to the database successful.")

    with conn.cursor() as cur:
        try:
            cur.execute(sql)
            rows = cur.fetchmany(limit+1)
        except psycopg.Error as e:
            raise QueryError(f"Database query error: {e}") from e

    return {"rows": rows[:limit], "row_count": len(rows[:limit]), "truncated": len(rows) > limit}

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

    for attempt in (1, 2):
        try:
            if conn is None or conn.closed:
                conn = connect()
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchmany(limit+1)
            break
        except psycopg.OperationalError as e:
            # Neon suspends idle compute after ~5 min, so the first query after a lull
            # finds a dead socket. Drop it and let the next pass reconnect.
            conn = None
            if attempt == 2:
                raise QueryError(f"Database query error: {e}") from e
        except psycopg.Error as e:
            raise QueryError(f"Database query error: {e}") from e

    return {"rows": rows[:limit], "row_count": len(rows[:limit]), "truncated": len(rows) > limit}

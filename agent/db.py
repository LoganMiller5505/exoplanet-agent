import sqlite3

class QueryError(Exception):
    pass

DB_PATH = "data/exoplanets.db"

def connect():
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True, timeout=5)
    conn.row_factory = sqlite3.Row
    return conn

def query(sql, limit=50):
    conn = connect()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = [dict(row) for row in cursor.fetchmany(limit+1)]
    except sqlite3.Error as e:
        raise QueryError(f"Database query error: {e}") from e
    finally:
        conn.close()

    return {"rows": rows[:limit], "row_count": len(rows[:limit]), "truncated": len(rows) > limit}

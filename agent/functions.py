import sqlite3

def get_habitable_planets(size_class=None):
    conn = sqlite3.connect('data/exoplanets.db')
    cursor = conn.cursor()

    query = "SELECT * FROM habitable"
    params = []

    if size_class:
        if size_class == 'small':
            query += " WHERE pl_rade BETWEEN 0 AND 1.5"
        elif size_class == 'medium':
            query += " WHERE pl_rade BETWEEN 1.5 AND 2.5"
        elif size_class == 'large':
            query += " WHERE pl_rade BETWEEN 2.5 AND 10"
        else:
            raise ValueError("Invalid size class. Choose from 'small', 'medium', or 'large'.")

    query += " LIMIT 20"

    cursor.execute(query, params)
    results = cursor.fetchall()

    conn.close()
    return results

TOOL_FUNCTIONS = {
    "get_habitable_planets": get_habitable_planets,
}
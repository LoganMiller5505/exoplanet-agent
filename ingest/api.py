import requests
import sqlite3

def get_planetary_systems_data():
    url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,pl_masse,ra,dec+from+ps+where+upper(soltype)+like+'%25CONF%25'+and+pl_masse+between+0.5+and+2.0&format=json"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Failed to fetch data. Status code: {response.status_code}")
        return None

def main():
    conn = sqlite3.connect("data/test.db")
    conn.execute("CREATE TABLE IF NOT EXISTS test (pl_name TEXT, pl_masse REAL, ra REAL, dec REAL);")
    data = get_planetary_systems_data()

    if data is None:
        print("No data to insert into the database.")
        return

    for item in data:
        conn.execute("INSERT INTO test (pl_name, pl_masse, ra, dec) VALUES (?, ?, ?, ?);", (item['pl_name'], item['pl_masse'], item['ra'], item['dec']))

    conn.commit()
    print("SQLite database successfully created")
    conn.close()

if __name__ == "__main__":
    main()
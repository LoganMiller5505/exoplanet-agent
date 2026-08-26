import requests
import sqlite3
import xml.etree.ElementTree as ET

TABLES_XML_PATH = "data/tables.xml"
XML_TYPE_MATCH = {"char": "TEXT", "double": "REAL", "int": "INTEGER"}

def get_ps_column_types(return_columns):
    tree = ET.parse(TABLES_XML_PATH)

    for table in tree.findall(".//table"):
        if table.findtext("name") == "ps":
            ps_columns = {column.findtext("name"): XML_TYPE_MATCH[column.findtext("dataType")] for column in table.findall("column")}
            return {column: ps_columns[column] for column in return_columns.split(",")}

def get_planetary_systems_data(return_columns="pl_name,disc_pubdate,disc_year,discoverymethod,disc_locale,disc_facility,disc_instrument,disc_telescope,sy_snum,sy_pnum,sy_mnum,cb_flag,ptv_flag,tran_flag,rv_flag,ast_flag,obm_flag,micro_flag,etv_flag,ima_flag,pul_flag,soltype,pl_controv_flag,pl_rade,pl_bmasse,pl_bmassprov,pl_orbeccenstr,pl_eqt,st_spectype,st_teff,st_rad,st_mass,st_met,st_metratio,st_logg,sy_dist,rowupdate,releasedate"):
    conn = sqlite3.connect("data/exoplanets.db")

    url = f"https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+{return_columns}+from+ps&format=json"
    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        column_types = get_ps_column_types(return_columns)
        definitions = ", ".join(f"{column} {column_type}" for column, column_type in column_types.items())
        conn.execute(f"CREATE TABLE IF NOT EXISTS ps ({definitions})")
        placeholders = ", ".join("?" for column in column_types)
        for item in json_data:
            conn.execute(f"INSERT INTO ps ({', '.join(column_types)}) VALUES ({placeholders})", tuple(item[column] for column in column_types))
        conn.commit()
        print(f"Data fetched and stored in the database successfully. Total records: {len(json_data)}")
    else:
        print(f"Error: Failed to fetch data. Status code: {response.status_code}")

def main():
    get_planetary_systems_data()

if __name__ == "__main__":
    main()

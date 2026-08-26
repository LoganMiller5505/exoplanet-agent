import requests
import sqlite3
import xml.etree.ElementTree as ET
import json

TABLES_XML_PATH = "data/tables.xml"
XML_TYPE_MATCH = {"char": "TEXT", "double": "REAL", "int": "INTEGER"}

ps_return_columns = """
    pl_name,hostname,pl_letter,default_flag,soltype,
    discoverymethod,disc_year,disc_facility,
    ra,dec,sy_dist,
    pl_orbper,pl_orbsmax,pl_orbeccen,
    pl_rade,pl_radj,pl_bmasse,pl_bmassj,pl_bmassprov,pl_eqt,pl_insol,
    st_spectype,st_teff,st_rad,st_mass,st_logg,st_met,
    sy_vmag,pl_controv_flag,rowupdate,
    tic_id,
    pl_orbincl,pl_dens,pl_trandep,pl_trandur,pl_tranmid,pl_ratror,
    st_lum,st_age,st_metratio,
    sy_kmag,sy_gaiamag,sy_tmag,
    sy_pnum,sy_snum,
    tran_flag,rv_flag,ttv_flag,ima_flag,micro_flag,
    pl_refname,disc_refname,pl_pubdate,
    hd_name,hip_name,gaia_dr3_id,
    disc_telescope,disc_instrument,disc_locale,disc_pubdate,
    sy_plx,sy_pm,st_dens,st_rotp,sy_mnum,
    ast_flag,obm_flag,etv_flag,ptv_flag,pul_flag,dkin_flag,cb_flag,
    pl_ntranspec,pl_nespec,pl_ndispec,
    st_refname,releasedate,
    pl_radeerr1,pl_radeerr2,pl_radelim,
    pl_bmasseerr1,pl_bmasseerr2,pl_bmasselim,
    pl_orbpererr1,pl_orbpererr2,pl_orbperlim,
    pl_orbsmaxerr1,pl_orbsmaxerr2,pl_orbsmaxlim,
    pl_orbeccenerr1,pl_orbeccenerr2,pl_orbeccenlim,
    pl_eqterr1,pl_eqterr2,pl_eqtlim,
    pl_insolerr1,pl_insolerr2,pl_insollim,
    st_tefferr1,st_tefferr2,st_masserr1,st_masserr2,st_raderr1,st_raderr2
""".replace("\n", "").replace(" ", "")

toi_return_columns = """
    toi,toipfx,tid,ctoi_alias,tfopwg_disp,pl_pnum,
    ra,dec,st_pmra,st_pmdec,
    pl_orbper,pl_tranmid,pl_trandurh,pl_trandep,pl_rade,pl_insol,pl_eqt,
    st_tmag,st_dist,st_teff,st_rad,st_logg,
    sectors,toi_created,rowupdate,release_date
""".replace("\n", "").replace(" ", "")

cumulative_return_columns = """
    kepid,kepoi_name,kepler_name,
    koi_disposition,koi_pdisposition,koi_disp_prov,koi_score,
    koi_fpflag_nt,koi_fpflag_ss,koi_fpflag_co,koi_fpflag_ec,
    koi_period,koi_time0bk,koi_duration,koi_depth,koi_prad,koi_sma,koi_teq,koi_insol,koi_ror,koi_incl,
    koi_steff,koi_srad,koi_smass,koi_slogg,koi_kepmag,ra,dec
""".replace("\n", "").replace(" ", "")

k2pandc_return_columns = """
    pl_name,hostname,epic_candname,epic_hostname,k2_name,
    default_flag,disposition,disp_refname,k2_campaigns,k2_campaigns_num,
    discoverymethod,disc_year,ra,dec,
    pl_orbper,pl_rade,pl_bmasse,pl_eqt,pl_insol,
    st_teff,st_rad,st_mass,sy_dist
""".replace("\n", "").replace(" ", "")

spectra_return_columns = """
    pl_name,spec_type,authors,num_datapoints,instrument,facility,
    mintranmid,maxtranmid,minwavelng,maxwavelng,note,bibcode,spec_path
""".replace("\n", "").replace(" ", "")

keplernames_return_columns = """
    kepid,pl_name,koi_name,kepler_name
""".replace("\n", "").replace(" ", "")

k2names_return_columns = """
    k2_name,pl_name,epic_id
""".replace("\n", "").replace(" ", "")

pscomppars_return_columns = """
    pl_name,hostname,pl_tsm,pl_esm,pl_angsep,
    pl_nobs_jwst_tran,pl_nobs_jwst_e,pl_nobs_jwst_pc,pl_nobs_jwst_di
""".replace("\n", "").replace(" ", "")

transitspec_return_columns = """
    plntname,centralwavelng,bandwidth,
    plntransdep,plntransdeperr1,plntransdeperr2,
    plnratror,plntranmid,
    facility,instrument,plntranreflink,rowupdate
""".replace("\n", "").replace(" ", "")

emissionspec_return_columns = """
    plntname,centralwavelng,bandwidth,
    especlipdep,especlipdeperr1,especlipdeperr2,espbritemp,
    facility,instrument,note,plntreflink,rowupdate
""".replace("\n", "").replace(" ", "")

nexolist_return_columns = """
    pl_name,hostname,event,program,observation_num,status,
    facility,instrument,observingmode,gratinggrism,
    observation_dur,starttime,endtime,pl_tsm,pl_esm
""".replace("\n", "").replace(" ", "")

def get_column_types(table_name, return_columns):
    tree = ET.parse(TABLES_XML_PATH)

    for table in tree.findall(".//table"):
        if table.findtext("name").lower() == table_name:
            ps_columns = {column.findtext("name"): XML_TYPE_MATCH[column.findtext("dataType")] for column in table.findall("column")}
            return {column: ps_columns[column] for column in return_columns.split(",")}

def get_exoplanet_data(table_name, return_columns):
    url = f"https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+{return_columns}+from+{table_name}&format=json"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: Failed to fetch data. Status code: {response.status_code}")
        return
    
    try:
        json_data = response.json()
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON when fetching data from {table_name}.\n{e}")
        return
    conn = sqlite3.connect("data/exoplanets.db")
    column_types = get_column_types(table_name, return_columns)
    definitions = ", ".join(f"{column} {column_type}" for column, column_type in column_types.items())
    with conn:
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.execute(f"CREATE TABLE {table_name} ({definitions})")
        placeholders = ", ".join("?" for column in column_types)
        conn.executemany(f"INSERT INTO {table_name} ({', '.join(column_types)}) VALUES ({placeholders})", [tuple(item[column] for column in column_types) for item in json_data])
    conn.commit()
    conn.close()
    print(f"{table_name} fetched and stored in the database successfully. Total records: {len(json_data)}")
        
def main():
    get_exoplanet_data("ps", ps_return_columns)
    get_exoplanet_data("toi", toi_return_columns)
    get_exoplanet_data("cumulative", cumulative_return_columns)
    get_exoplanet_data("k2pandc", k2pandc_return_columns)
    get_exoplanet_data("spectra", spectra_return_columns)
    get_exoplanet_data("keplernames", keplernames_return_columns)
    get_exoplanet_data("k2names", k2names_return_columns)
    get_exoplanet_data("pscomppars", pscomppars_return_columns)
    get_exoplanet_data("transitspec", transitspec_return_columns)
    get_exoplanet_data("emissionspec", emissionspec_return_columns)
    get_exoplanet_data("nexolist", nexolist_return_columns)

if __name__ == "__main__":
    main()

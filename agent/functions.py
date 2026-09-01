import re
from db import query

# Shared functions (not directly called by tools)
def resolve_object(name):
    norm_name = re.sub(r'[^a-zA-Z0-9]', '', name).lower()
    query_str = f"""
        SELECT
            resolves_to,
            pl_name,
            hostname,
            GROUP_CONCAT(DISTINCT alias_type) AS matched_via,
            MIN(alias) AS matched_alias
        FROM planet_names
        WHERE alias_norm LIKE '{norm_name}'
        GROUP BY resolves_to, pl_name, hostname
    """
    result = query(query_str)
    rows = result["rows"]

    if not rows:
        query_str = f"""
            SELECT
                resolves_to,
                pl_name,
                hostname,
                GROUP_CONCAT(DISTINCT alias_type) AS matched_via,
                MIN(alias) AS matched_alias
            FROM planet_names
            WHERE alias_norm LIKE '{norm_name}%'
            GROUP BY resolves_to, pl_name, hostname
        """
        result = query(query_str, limit=8)
        rows = result["rows"]

        status = "suggestions" if rows else "not_found"
        resolves_to = None
        pl_name = None
        hostname = None
        candidates = rows if rows else []
        matched_via = None
    else:
        status = "resolved" if len(rows) == 1 else "ambiguous"
        resolves_to = rows[0]["resolves_to"]
        pl_name = rows[0]["pl_name"]
        hostname = rows[0]["hostname"]
        candidates = rows
        matched_via = rows[0]["matched_via"]

    return {"status": status, "resolves_to": resolves_to, "pl_name": pl_name, "hostname": hostname, "candidates": candidates, "matched_via": matched_via}

def _sql_escape(value):
    # Double any single quote so names like "Barnard's star" work
    return value.replace("'", "''")


_RESOLVE_NOTES = {
    "ambiguous": "'{name}' matches more than one object; ask which was meant before answering.",
    "suggestions": "No exact match for '{name}'. The candidates below merely start with it -- confirm one before using it.",
    "not_found": "No object named '{name}' in the archive.",
}

# Single-return functions (called by tools)
def get_planet(name):
    resolved = resolve_object(name)

    # Hand off to get_system if the name resolves to a star
    if resolved["status"] == "resolved" and resolved["resolves_to"] == "star":
        return {
            "status": "is_star",
            "hostname": resolved["hostname"],
            "system": get_system(resolved["hostname"]),
            "notes": [f"'{name}' names a star, not a planet. Returning its system instead."],
        }

    # Any ambiguity needs to be brought to the user first
    if resolved["status"] != "resolved":
        return {
            "status": resolved["status"],
            "candidates": resolved["candidates"],
            "notes": [_RESOLVE_NOTES[resolved["status"]].format(name=name)],
        }

    query_str = f"""
        SELECT
            p.pl_name               AS pl_name,
            p.hostname              AS hostname,
            p.pl_letter             AS pl_letter,
            p.pl_rade               AS radius_earth,
            p.pl_bmasse             AS mass_earth,
            p.pl_orbper             AS orbital_period_days,
            p.pl_orbeccen           AS eccentricity,
            p.pl_eqt                AS equilibrium_temp_k,
            p.pl_insol              AS insolation_earth,
            p.sy_dist               AS distance_pc,
            p.discoverymethod       AS discovery_method,
            p.disc_year             AS discovery_year,
            p.disc_facility         AS discovery_facility,
            p.st_spectype           AS star_spectral_type,
            p.st_teff               AS star_temp_k,
            p.st_rad                AS star_radius_solar,
            p.st_mass               AS star_mass_solar,
            p.pl_tsm                AS tsm,
            p.pl_esm                AS esm,
            pc.size_class           AS size_class,
            pc.mass_class           AS mass_class,
            pc.orbital_class        AS orbital_class,
            pc.spectral_class       AS spectral_class,
            pc.is_giant             AS is_giant,
            pc.in_radius_valley     AS in_radius_valley,
            hz.orbsmax_au           AS semi_major_axis_au,
            hz.in_hz_conservative   AS in_hz_conservative,
            hz.in_hz_optimistic     AS in_hz_optimistic,
            hz.hz_position          AS hz_position,
            hz.is_rocky_candidate   AS is_rocky_candidate,
            -- Provenance and caveat flags, consumed by _planet_notes.
            p.pl_controv_flag       AS controversial,
            pc.mass_is_lower_bound  AS mass_is_lower_bound,
            hz.teff_in_valid_range  AS teff_in_valid_range,
            hz.lum_source           AS lum_source,
            hz.orbsmax_source       AS orbsmax_source
        FROM planets p
        LEFT JOIN planet_classes pc ON p.pl_name = pc.pl_name
        LEFT JOIN habitable_zone hz ON p.pl_name = hz.pl_name
        WHERE p.pl_name = '{_sql_escape(resolved["pl_name"])}'
    """

    # The name resolves to a planet, so query the planets view for its row
    rows = query(query_str)["rows"]
    if not rows:
        return {
            "status": "not_found",
            "candidates": [],
            "notes": [
                f"'{resolved['pl_name']}' is a known alias but has no row in the "
                "planetary systems catalog."
            ],
        }
    row = rows[0]

    # Attach necessary notes about return info, if any apply
    notes = []
    if row["controversial"] == 1:
        notes.append("This planet's existence is disputed in the literature.")
    if row["mass_is_lower_bound"] == 1:
        notes.append("Mass is a lower bound (M*sin i) from radial velocity, not a true mass.")
    if row["orbsmax_source"] == "derived":
        notes.append("Semi-major axis was derived from Kepler's third law, not measured.")
    if row["lum_source"] == "derived":
        notes.append("Stellar luminosity was derived from radius and temperature, not measured.")
    if row["teff_in_valid_range"] == 0:
        notes.append(
            "Host star temperature is outside the 2600-7200 K range of the habitable "
            "zone model, so habitable zone membership was NOT evaluated. Absent "
            "habitable zone fields mean 'unknown', not 'no'."
        )
    elif row["teff_in_valid_range"] is None:
        notes.append(
            "Habitable zone could not be computed (missing stellar luminosity or "
            "orbital distance). Absent habitable zone fields mean 'unknown', not 'no'."
        )

    # Do not directly return null values (handle separately)
    planet = {key: value for key, value in row.items() if value is not None}
    unavailable = [key for key, value in row.items() if value is None]

    return {
        "status": "resolved",
        "pl_name": row["pl_name"],
        "hostname": row["hostname"],
        "planet": planet,
        "fields_unavailable": unavailable,
        "notes": notes,
    }

def get_system(hostname):
    resolved = resolve_object(hostname)

    # Any ambiguity needs to be brought to the user first
    if resolved["status"] != "resolved":
        return {
            "status": resolved["status"],
            "candidates": resolved["candidates"],
            "notes": [_RESOLVE_NOTES[resolved["status"]].format(name=hostname)],
        }

    query_str = f"""
        SELECT *
        FROM systems
        WHERE hostname = '{_sql_escape(resolved["hostname"])}'
    """
    rows = query(query_str)["rows"]
    if not rows:
        return {
            "status": "not_found",
            "candidates": [],
            "notes": [
                f"'{resolved['hostname']}' is a known alias but has no row in the "
                "systems view."
            ],
        }
    row = rows[0]

    query_str = f"""
        SELECT
            p.pl_name,
            p.pl_letter,
            pc.size_class,
            pc.orbital_class,
            hz.orbsmax_au,
            hz.in_hz_conservative,
            hz.hz_position
        FROM planets p
        LEFT JOIN planet_classes pc ON p.pl_name = pc.pl_name
        LEFT JOIN habitable_zone hz ON p.pl_name = hz.pl_name
        WHERE p.hostname = '{_sql_escape(resolved["hostname"])}'
        ORDER BY hz.orbsmax_au NULLS LAST, p.pl_orbper
    """
    planets = query(query_str)["rows"]

    # Attach necessary notes about return info, if any apply
    notes = []
    if row["pnum_disagrees"] == 1:
        notes.append(
            f"The catalog lists {row['sy_pnum']} planets for this system but only "
            f"{row['num_planets']} have rows here."
        )
    if row["is_multi_star"] == 1:
        notes.append(
            f"Multi-star system ({row['sy_snum']} stars). Habitable zone boundaries "
            "assume a single host star, so they are less reliable here."
        )
    unevaluated = sum(1 for planet in planets if planet["in_hz_conservative"] is None)
    if unevaluated:
        notes.append(
            f"Habitable zone was NOT evaluated for {unevaluated} of {len(planets)} "
            "planets (host star outside the model's range, or missing luminosity or "
            "orbit). The system's n_in_hz_conservative and has_habitable_planet "
            "columns count only confirmed matches, so 0 means 'none confirmed', "
            "not 'none habitable'."
        )

    # Do not directly return null values (handle separately)
    system = {key: value for key, value in row.items() if value is not None}
    unavailable = [key for key, value in row.items() if value is None]

    return {
        "status": "resolved",
        "hostname": row["hostname"],
        "system": system,
        "planets": planets,
        "fields_unavailable": unavailable,
        "notes": notes,
    }


# General-purpose search function (called by tools)
def search_planets(
        radius_min=None, radius_max=None,
        mass_min=None, mass_max=None,
        period_min=None, period_max=None,
        distance_max_pc=None,
        size_class=None,
        orbital_class=None,
        spectral_class=None,
        discovery_method=None,
        disc_year_min=None, disc_year_max=None,
        in_habitable_zone=None,
        rocky_only=False,
        exclude_controversial=True,
        sort_by="distance_pc", limit=20
):
    FILTERS = {

    }
    return None


# Aggregate function (called by tools)
def count_planets(group_by, filters):
    # TODO: Implement a function to count planets based on groupings and filters
    return None


# "Meta" function (called by tools, if necessary)
def describe_schema(view=None):
    # TODO: Implement a function to describe the schema of the database
    return None


# Dictionary defining which functions are available to the tool
TOOL_FUNCTIONS = {
    "get_planet": get_planet,
    "get_system": get_system,
    "search_planets": search_planets,
    "count_planets": count_planets,
    "describe_schema": describe_schema,
}
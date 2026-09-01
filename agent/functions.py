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


# Single-return functions (called by tools)
def get_planet(name):
    name = resolve_object(name)
    # TODO: Finish implementation
    return None

def get_system(hostname):
    name = resolve_object(hostname)
    # TODO: Finish implementation
    return None


# General-purpose search function (called by tools)
def search_planets(**filters):
    # TODO: Implement a function to search for planets based on various filters (e.g., size, temperature, habitability)
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
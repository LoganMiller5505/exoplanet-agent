import sqlite3
import re

# Shared functions (not directly called by tools)
def resolve_object(name):
    norm_name = re.sub(r'[^a-zA-Z0-9]', '', name)
    # TODO: Implement a function to resolve an object name to a canonical form
    query = f"SELECT * FROM planets WHERE pl_name LIKE {norm_name}"
    return query(query)


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
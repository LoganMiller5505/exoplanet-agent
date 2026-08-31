tools = [
    {
        "type":"function",
        "function": {
            "name": "get_planet",
            "description": "Get detailed information about a specific planet by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the planet to retrieve information for.",
                    }
                },
                "required": ["name"]
            }
        }
    },
    {
        "type":"function",
        "function": {
            "name": "get_system",
            "description": "Get detailed information about a specific planetary system by its host star name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "hostname": {
                        "type": "string",
                        "description": "The name of the host star to retrieve information for.",
                    }
                },
                "required": ["hostname"]
            }
        }
    },
    {
        "type":"function",
        "function": {
            "name": "search_planets",
            "description": "Search for planets based on various filters (e.g., size, temperature, habitability).",
            "parameters": {
                "type": "object",
                "properties": {
                    "filters": {
                        "type": "object",
                        "description": "A dictionary of filters to apply to the search.",
                    }
                },
                "required": ["filters"]
            }
        }
    },
    {
        "type":"function",
        "function": {
            "name": "count_planets",
            "description": "Count the number of planets based on groupings and filters.",
            "parameters": {
                "type": "object",
                "properties": {
                    "group_by": {
                        "type": "string",
                        "description": "The field to group the count by.",
                    },
                    "filters": {
                        "type": "object",
                        "description": "A dictionary of filters to apply to the count.",
                    }
                },
                "required": ["group_by", "filters"]
            }
        }
    },
    {
        "type":"function",
        "function": {
            "name": "describe_schema",
            "description": "Describe the schema of the database, optionally for a specific view.",
            "parameters": {
                "type": "object",
                "properties": {
                    "view": {
                        "type": "string",
                        "description": "The name of the view to describe (optional).",
                    }
                },
                "required": []
            }
        }
    }
]
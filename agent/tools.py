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
            "description": "Search for planets based on various filters (e.g., size, distance, habitability). All filters are optional and combine with AND.",
            "parameters": {
                "type": "object",
                "properties": {
                    "radius_min": {
                        "type": "number",
                        "description": "Minimum planet radius, in Earth radii.",
                    },
                    "radius_max": {
                        "type": "number",
                        "description": "Maximum planet radius, in Earth radii.",
                    },
                    "mass_min": {
                        "type": "number",
                        "description": "Minimum planet mass, in Earth masses.",
                    },
                    "mass_max": {
                        "type": "number",
                        "description": "Maximum planet mass, in Earth masses.",
                    },
                    "period_min": {
                        "type": "number",
                        "description": "Minimum orbital period, in days.",
                    },
                    "period_max": {
                        "type": "number",
                        "description": "Maximum orbital period, in days.",
                    },
                    "distance_max_pc": {
                        "type": "number",
                        "description": "Maximum distance from Earth, in parsecs.",
                    },
                    "size_class": {
                        "type": "string",
                        "enum": ["terrestrial", "super_earth", "mini_neptune", "neptune_like", "gas_giant"],
                        "description": "Planet size category, derived from radius.",
                    },
                    "orbital_class": {
                        "type": "string",
                        "enum": ["ultra_short_period", "hot_jupiter", "warm_giant", "cold_giant", "hot_small", "other"],
                        "description": "Orbital regime category.",
                    },
                    "spectral_class": {
                        "type": "string",
                        "enum": ["O", "B", "A", "F", "G", "K", "M", "L/T/Y"],
                        "description": "Spectral type of the host star.",
                    },
                    "discovery_method": {
                        "type": "string",
                        "enum": ["Transit", "Radial Velocity", "Microlensing", "Imaging", "Astrometry",
                                 "Eclipse Timing Variations", "Transit Timing Variations",
                                 "Pulsar Timing", "Pulsation Timing Variations",
                                 "Orbital Brightness Modulation", "Disk Kinematics"],
                        "description": "Method by which the planet was discovered.",
                    },
                    "disc_year_min": {
                        "type": "integer",
                        "description": "Earliest discovery year.",
                    },
                    "disc_year_max": {
                        "type": "integer",
                        "description": "Latest discovery year.",
                    },
                    "in_habitable_zone": {
                        "type": "boolean",
                        "description": "True for planets inside the conservative habitable zone; false for planets that were evaluated and found outside it. Planets whose habitable zone could not be computed are excluded either way -- omit this filter to include them.",
                    },
                    "rocky_only": {
                        "type": "boolean",
                        "description": "Restrict to planets that are rocky candidates. Defaults to false.",
                    },
                    "exclude_controversial": {
                        "type": "boolean",
                        "description": "Exclude planets flagged as controversial. Defaults to true.",
                    },
                    "sort_by": {
                        "type": "string",
                        "enum": ["distance_pc", "radius_earth", "mass_earth", "orbital_period_days", "discovery_year", "hz_position"],
                        "description": "Column to sort results by. Defaults to distance_pc.",
                    },
                    "sort_desc": {
                        "type": "boolean",
                        "description": "Sort descending instead of ascending. Set true for superlatives -- largest, most massive, longest period, most recent, farthest. Defaults to false (smallest/nearest/oldest first).",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of planets to return. Defaults to 20.",
                    }
                },
                "required": []
            }
        }
    },
    {
        "type":"function",
        "function": {
            "name": "count_planets",
            "description": "Count planets, optionally grouped by a column. Takes the same filters as search_planets. Omit group_by for a single total.",
            "parameters": {
                "type": "object",
                "properties": {
                    "group_by": {
                        "type": "string",
                        "enum": ["size_class", "mass_class", "orbital_class", "spectral_class",
                                 "discovery_method", "discovery_year", "in_habitable_zone",
                                 "hostname"],
                        "description": "Column to group counts by. Omit for a single total across all matching planets.",
                    },
                    "radius_min": {
                        "type": "number",
                        "description": "Minimum planet radius, in Earth radii.",
                    },
                    "radius_max": {
                        "type": "number",
                        "description": "Maximum planet radius, in Earth radii.",
                    },
                    "mass_min": {
                        "type": "number",
                        "description": "Minimum planet mass, in Earth masses.",
                    },
                    "mass_max": {
                        "type": "number",
                        "description": "Maximum planet mass, in Earth masses.",
                    },
                    "period_min": {
                        "type": "number",
                        "description": "Minimum orbital period, in days.",
                    },
                    "period_max": {
                        "type": "number",
                        "description": "Maximum orbital period, in days.",
                    },
                    "distance_max_pc": {
                        "type": "number",
                        "description": "Maximum distance from Earth, in parsecs.",
                    },
                    "size_class": {
                        "type": "string",
                        "enum": ["terrestrial", "super_earth", "mini_neptune", "neptune_like", "gas_giant"],
                        "description": "Planet size category, derived from radius.",
                    },
                    "orbital_class": {
                        "type": "string",
                        "enum": ["ultra_short_period", "hot_jupiter", "warm_giant", "cold_giant", "hot_small", "other"],
                        "description": "Orbital regime category.",
                    },
                    "spectral_class": {
                        "type": "string",
                        "enum": ["O", "B", "A", "F", "G", "K", "M", "L/T/Y"],
                        "description": "Spectral type of the host star.",
                    },
                    "discovery_method": {
                        "type": "string",
                        "enum": ["Transit", "Radial Velocity", "Microlensing", "Imaging", "Astrometry",
                                 "Eclipse Timing Variations", "Transit Timing Variations",
                                 "Pulsar Timing", "Pulsation Timing Variations",
                                 "Orbital Brightness Modulation", "Disk Kinematics"],
                        "description": "Method by which the planet was discovered.",
                    },
                    "disc_year_min": {
                        "type": "integer",
                        "description": "Earliest discovery year.",
                    },
                    "disc_year_max": {
                        "type": "integer",
                        "description": "Latest discovery year.",
                    },
                    "in_habitable_zone": {
                        "type": "boolean",
                        "description": "True for planets inside the conservative habitable zone; false for planets that were evaluated and found outside it. Planets whose habitable zone could not be computed are excluded either way -- omit this filter to include them.",
                    },
                    "rocky_only": {
                        "type": "boolean",
                        "description": "Restrict to planets that are rocky candidates. Defaults to false.",
                    },
                    "exclude_controversial": {
                        "type": "boolean",
                        "description": "Exclude planets flagged as controversial. Defaults to true.",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of groups to return. Defaults to 50.",
                    }
                },
                "required": []
            }
        }
    }
]
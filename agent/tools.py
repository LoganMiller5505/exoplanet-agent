tools = [
    {
        "type": "function",
        "function": {
            "name": "get_habitable_planets",
            "description": "Get a list of habitable planets based on their equilibrium temperature.",
            "parameters": {
                "type": "object",
                "properties": {
                    "size_class": {
                        "type": "string",
                        "description": "The size class of the planets to filter by. Options are 'small', 'medium', or 'large'.",
                    }
                },
                "required": []
            }
        }
    }
]
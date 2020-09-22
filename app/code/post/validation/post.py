CREATE_POST_SCHEMA = {
    "type": "object",
    "properties": {
        "slug": {
            "type": "string",
            "minLength": 2
        },
        "url": {
            "type": "string",
            "minLength": 3,
        },
        "poster": {
            "type": "string",
            "minLength": 10,
        },
        "category": {
            "type": "number",
        },
        "tags": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "number"
            }
        }
    },
    "required": [
        "slug",
        "url",
        "category"
    ],
    "additionalProperties": False
}

DELETE_POST_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "number",
        },
    },
    "required": [
        "id",
    ],
    "additionalProperties": False
}

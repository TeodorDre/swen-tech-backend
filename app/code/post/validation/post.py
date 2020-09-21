CREATE_POST_SCHEMA = {
    "type": "object",
    "properties": {
        "slug": {
            "type": "string",
            "minLength": 2
        },
    },
    "required": [
        "slug",
        "translations",
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

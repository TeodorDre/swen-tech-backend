CREATE_TAG_SCHEMA = {
    "type": "object",
    "properties": {
        "slug": {
            "type": "string",
            "minLength": 2
        },
        "translations": {
            "type": "array",
            "minItems": 3,
            "items": {
                "type": "string"
            }
        }
    },
    "required": [
        "slug",
        "translations",
    ],
    "additionalProperties": False
}

DELETE_TAG_SCHEMA = {
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

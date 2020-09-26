CREATE_POST_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "minLength": 2
        },
        "poster": {
            "type": "string",
            "minLength": 10,
        },
        "posterAltText": {
          "type:": "string",
          "minLength": 5,
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
        "title",
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

CREATE_POST_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {
            "type": "array",
            "minItems": 3,
            "items": {
                "type": "string"
            }
        },
        "body": {
            "type": "array",
            "minItems": 3,
            "items": {
                "type": "string"
            }
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
        "category",
        "body",
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

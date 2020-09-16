CREATE_TAG_SCHEMA = {
    "type": "object",
    "properties": {
        "slug": {
            "type": "string",
            "minLength": 2
        },
        "nameRu": {
            "type": "string"
        },
        "nameEn": {
            "type": "string"
        },
        "nameFr": {
            "type": "string"
        },

    },
    "required": [
        "slug",
        "nameRu",
        "nameEn",
        "nameFr",
    ],
    "additionalProperties": False
}

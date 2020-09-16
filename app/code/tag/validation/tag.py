CREATE_TAG_SCHEMA = {
    "type": "object",
    "properties": {
        "slug": {
            "type": "string",
            "minLength": 2
        },
        "translations": {
            "type": "array",
            "minItems": 1,
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

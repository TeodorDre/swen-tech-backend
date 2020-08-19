SCHEMA = {
    # PROJECTS
    'project_post': {
        "type": "object",
        "properties": {
            "project_name": {
                "type": "string",
                "minLength": 5,
                "description": "The project name."
            },
            "project_description": {
                "type": "string"
            }
        },
        "required": [
            "project_name"
        ],
        "additionalProperties": False
    },
    'project_update': {
        "type": "object",
        "properties": {
            "project_id": {
                "type": "integer"
            },
            "project_name": {
                "type": "string",
                "description": "The project name."
            },
            "project_description": {
                "type": "string"
            }
        },
        "required": [
            "project_id"
        ],
        "additionalProperties": False
    },
    'project_delete': {
        "type": "object",
        "properties": {
            "project_id": {
                "type": "integer"
            }
        },
        "required": [
            "project_id"
        ],
        "additionalProperties": False
    },
    # DATASETS
    'dataset_post': {
        "type": "object",
        "properties": {
            "dataset_name": {
                "type": "string",
                "minLength": 5,
                "description": "The dataset name."
            },
            "dataset_description": {
                "type": "string"
            },
            "project_id": {
                "type": "integer",
                "description": "Project id."
            }
        },
        "required": [
            "dataset_name",
            "project_id"
        ],
        "additionalProperties": False
    },
    'dataset_get': {
        "type": "object",
        "properties": {
            "project_id": {
                "type": "integer",
                "description": "Project id."
            }
        },
        "required": [
            "project_id"
        ],
        "additionalProperties": False
    },
    'dataset_update': {
        "type": "object",
        "properties": {
            "dataset_id": {
                "type": "integer"
            },
            "dataset_name": {
                "type": "string",
                "minLength": 5,
                "description": "The project name."
            },
            "dataset_description": {
                "type": "string"
            },
            "project_id": {
                "type": "integer",
                "description": "Project id."
            }
        },
        "required": [
            "dataset_id"
        ],
        "additionalProperties": False
    },
    'dataset_delete': {
        "type": "object",
        "properties": {
            "dataset_id": {
                "type": "integer"
            }
        },
        "required": [
            "dataset_id"
        ],
        "additionalProperties": False
    },
    # IMAGES
    'image_post': {
        "type": "object",
        "properties": {
            "image_name": {
                "type": "string",
                "minLength": 5,
                "description": "The image name."
            },
            "image_description": {
                "type": "string"
            },
            "image_link": {
                "type": "string"
            },
            "width": {
                "type": "integer",
            },
            "height": {
                "type": "integer",
            },
            "dataset_id": {
                "type": "integer",
                "description": "Dataset id."
            }
        },
        "required": [
            "image_name",
            "dataset_id",
            "image_link",
            "width",
            "height"
        ],
        "additionalProperties": False
    },
    'image_get': {
        "type": "object",
        "properties": {
            "dataset_id": {
                "type": "integer",
                "description": "Dataset id."
            }
        },
        "required": [
            "dataset_id"
        ],
        "additionalProperties": False
    },
    'image_update': {
        "type": "object",
        "properties": {
            "image_id": {
                "type": "integer"
            },
            "image_name": {
                "type": "string",
                "minLength": 5,
                "description": "The image name."
            },
            "image_description": {
                "type": "string"
            },
            "image_link": {
                "type": "string"
            },
            "width": {
                "type": "integer",
            },
            "height": {
                "type": "integer",
            },
            "dataset_id": {
                "type": "integer",
                "description": "Dataset id."
            }
        },
        "required": [
            "image_id"
        ],
        "additionalProperties": False
    },
    'image_delete': {
        "type": "object",
        "properties": {
            "image_id": {
                "type": "integer"
            }
        },
        "required": [
            "image_id"
        ],
        "additionalProperties": False
    },
    # LABELS
    'label_post': {
        "type": "object",
        "properties": {
            "label_name": {
                "type": "string",
                "minLength": 5,
                "description": "The label name."
            },
            "label_description": {
                "type": "string"
            },
            "color": {
                "type": "string"
            },
            "parameters": {
                "type": "object"
            }
        },
        "required": [
            "label_name",
            "color",
        ],
        "additionalProperties": False
    },
    'label_get': {
        "type": "object",
        "properties": {
            "label_id": {
                "type": "integer",
                "description": "Label id."
            }
        },
        "required": [
            "label_id"
        ],
        "additionalProperties": False
    },
    'label_update': {
        "type": "object",
        "properties": {
            "label_id": {
                "type": "integer"
            },
            "label_name": {
                "type": "string",
                "description": "The label name."
            },
            "label_description": {
                "type": "string"
            },
            "color": {
                "type": "string"
            },
            "parameters": {
                "type": "object"
            }
        },
        "required": [
            "label_id"
        ],
        "additionalProperties": False
    },
    'label_delete': {
        "type": "object",
        "properties": {
            "label_id": {
                "type": "integer"
            }
        },
        "required": [
            "label_id"
        ],
        "additionalProperties": False
    },
    # ANNOTATIONS
    'annotation_post': {
        "type": "object",
        "properties": {
            "image_id": {
                "type": "integer",
            },
            "annotations": {
                "type": "object",
            }
        },
        "required": [
            "image_id",
            "annotations",
        ],
        "additionalProperties": False
    },
    'annotation_get': {
        "type": "object",
        "properties": {
            "image_id": {
                "type": "integer",
            }
        },
        "required": [
            "image_id"
        ],
        "additionalProperties": False
    },
    'annotation_update': {
        "type": "object",
        "properties": {
            "image_id": {
                "type": "integer",
            },
            "annotations": {
                "type": "object"
            }
        },
        "required": [
            "image_id",
            "annotations",
        ],
        "additionalProperties": False
    },
    'annotation_delete': {
        "type": "object",
        "properties": {
            "image_id": {
                "type": "integer"
            }
        },
        "required": [
            "image_id"
        ],
        "additionalProperties": False
    }
}

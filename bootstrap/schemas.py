import os
import json

from psycopg2.extras import Json
from mimesis import Text
from mimesis import Internet
from random import randint
from mimesis.schema import Field

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT = Text('en')
DUMMY = Field('en')
IMG = Internet()

WIDTH = 1920
HEIGHT = 1080
SCHEMA = 'markup'

with open(os.path.join(BASE_DIR, 'sample_annotation.json')) as stream:
    SAMPLE = json.load(stream)

# TEAMS = {
#     'fields': (lambda: {'team_name': DUMMY('text.word')}),
#     'quantity': 3,
#     'schema': SCHEMA,
#     'table': 'teams',
#     'values': '(team_name)',
#     'template': '(%(team_name)s)'
# }
# USERS = {
#     'fields': (
#         lambda: {'team_id': randint(1, TEAMS['quantity']),
#                  'username': DUMMY('text.word'),
#                  'email': DUMMY('person.email', key=str.lower),
#                  'password': DUMMY('token'), }),
#     'quantity': 10,
#     'schema': SCHEMA,
#     'table': 'users',
#     'values': '(team_id, username, email, password)',
#     'template': '(%(team_id)s, %(username)s, %(email)s, %(password)s)'
#
# }

PROJECTS = {
    'fields': lambda: {'project_name': DUMMY('text.word'),
                       'project_description': TEXT.text(quantity=randint(1, 4)),
                       # 'team_id': randint(1, TEAMS['quantity'])
                       },
    'quantity': 3,
    'schema': SCHEMA,
    'table': 'projects',
    'values': '(project_name, project_description)',
    'template': '(%(project_name)s, %(project_description)s)',
    # 'values': '(project_name, project_description, team_id)',
    # 'template': '(%(project_name)s, %(project_description)s, %(team_id)s)'
}
DATASETS = {
    'fields': lambda: {'dataset_name': DUMMY('text.word'),
                       'dataset_description': TEXT.text(quantity=randint(1, 4)),
                       'dataset_tags': TEXT.words(quantity=randint(1, 3)),
                       'project_id': randint(1, PROJECTS['quantity'])},
    'quantity': 10,
    'schema': SCHEMA,
    'table': 'datasets',
    'values': '(dataset_name, dataset_description, dataset_tags, project_id)',
    'template': '(%(dataset_name)s, %(dataset_description)s, %(dataset_tags)s, %(project_id)s)'
}
LABELS = {
    'fields': lambda: {'label_name': DUMMY('text.word'),
                       'label_description': TEXT.text(quantity=randint(1, 4)),
                       'color': TEXT.color()},
    'quantity': 10,
    'schema': SCHEMA,
    'table': 'labels',
    'values': '(label_name, label_description, color)',
    'template': '(%(label_name)s, %(label_description)s, %(color)s)'

}
IMAGES = {
    'fields': lambda: {'image_name': DUMMY('text.word'),
                       'image_description': TEXT.text(quantity=randint(1, 4)),
                       'image_link': IMG.stock_image(width=WIDTH, height=HEIGHT),
                       'width': WIDTH,
                       'height': HEIGHT,
                       'dataset_id': randint(1, DATASETS['quantity'])},
    'quantity': 1000,
    'schema': SCHEMA,
    'table': 'images',
    'values': '(image_name, image_description, image_link, width, height, dataset_id)',
    'template': '(%(image_name)s, %(image_description)s, %(image_link)s, %(width)s, %(height)s, %(dataset_id)s)'
}
ANNOTATIONS = {
    'fields': lambda: {'image_id': randint(1, IMAGES['quantity']),
                       'annotations': Json(SAMPLE)
                       },
    'quantity': 30,
    'schema': SCHEMA,
    'table': 'annotations',
    'values': '(image_id, annotations)',
    'template': '(%(image_id)s, %(annotations)s)'
}

SCHEMAS = [PROJECTS, DATASETS, LABELS, IMAGES, ANNOTATIONS]

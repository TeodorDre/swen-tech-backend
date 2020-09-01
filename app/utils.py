from aiohttp import web
import string
import random
from app.statuscodes import *


def send_not_found_response():
    return web.json_response({
        'result': 'error',
        'code': 1,
        'message': 'Incorrect password or email.'
    }, status=OK)


def send_unexpected_error_response():
    return web.json_response({
        'result': 'error',
        'code': 25,
        'message': 'Unexpected error.'
    }, status=OK)


def generate_id(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

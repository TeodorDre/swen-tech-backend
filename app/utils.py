from aiopg.sa import create_engine
from aiohttp import web
import datetime
import string
import random
from app.statuscodes import *


async def init_pg(app):
    # conf = app['config']['postgres']
    conf = app['config']
    engine = await create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        # minsize=conf['minsize'],
        # maxsize=conf['maxsize'],
        loop=app.loop)
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


def dt_converter(dt):
    if isinstance(dt, datetime.datetime):
        return dt.__str__()


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

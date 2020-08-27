from aiohttp import web
import logging

AUTH_HANDLERS = []


@web.middleware
async def json_checker(request, handler):
    logging.info(f'New request for handler: {handler.__name__}')

    return await handler(request)

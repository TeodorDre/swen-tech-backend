from enum import Enum
from aiohttp import web
from app.base.network import HTTPStatusCode


class APIErrorCode(Enum):
    BadRequest = 1,
    UnexpectedError = 25


def send_not_found_response():
    return web.json_response({
        'result': 'error',
        'code': APIErrorCode.BadRequest,
        'message': 'Incorrect password or email.'
    }, status=HTTPStatusCode.OK)


def send_unexpected_error_response():
    return web.json_response({
        'result': 'error',
        'code': APIErrorCode.UnexpectedError,
        'message': 'Unexpected error.'
    }, status=HTTPStatusCode.OK)

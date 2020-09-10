from enum import Enum
from aiohttp import web
from app.base.network import HTTPStatusCode


class APIErrorCode(Enum):
    BadRequest = 1,
    NotFoundError = 2,
    UnexpectedError = 25


def send_success_response(request_name: str, result) -> web.Response:
    return web.json_response({
        'request': request_name,
        'result': result
    }, status=HTTPStatusCode.OK.value[0])


def send_not_found_response(request_name: str, error_message: str = 'Not found') -> web.Response:
    return web.json_response({
        'request': request_name,
        'errorCode': APIErrorCode.NotFoundError.value[0],
        'errorMessage': error_message
    }, status=HTTPStatusCode.OK.value[0])


def bad_request_response(request_name: str, error_message: str = 'Bad request') -> web.Response:
    return web.json_response({
        'request': request_name,
        'errorCode': APIErrorCode.BadRequest.value[0],
        'errorMessage': error_message
    })


def send_unexpected_error_response(request_name: str, ) -> web.Response:
    return web.json_response({
        'request': request_name,
        'errorCode': APIErrorCode.UnexpectedError.value[0],
        'errorMessage': 'Unexpected error.'
    }, status=HTTPStatusCode.OK.value[0])

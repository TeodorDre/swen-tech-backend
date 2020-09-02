from aiohttp import web
from app.base.network import HTTPStatusCode

__all__ = [
    'echo', 'variable_handler',
]


async def echo() -> web.Response:
    return web.json_response({'status': 'OK'}, status=HTTPStatusCode.OK)


async def variable_handler(request) -> web.Response:
    return web.json_response({'error': f"Path: '{request.match_info['name']}' does't available"},
                             status=HTTPStatusCode.NOT_FOUND)

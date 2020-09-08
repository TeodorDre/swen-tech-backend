from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.base.network import HTTPStatusCode


class VariableRouteHandler(RouteHandler):
    def __init__(self, log_service: LogService):
        super().__init__(log_service)

        self.path = '/{name}'
        self.request_type = hdrs.METH_GET

        self.name = 'common.variable'

    def handler(self, request: web.Request) -> web.Response:
        self.log_service.info('VariableRouteHandler - variable called')

        return web.json_response({'error': f"Path: '{request.match_info['name']}' does't available"},
                                 status=HTTPStatusCode.NOT_FOUND.value[0])

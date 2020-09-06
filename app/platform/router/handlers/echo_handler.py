from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web
from app.base.network import HTTPStatusCode


class EchoRouteHandler(RouteHandler):
    def __init__(self, log_service: LogService):
        super().__init__(log_service)

        self.path = '/echo'

    def handler(self) -> web.Response:
        self.log_service.info('EchoRouteHandler - echo called')

        return web.json_response({'status': 'OK'}, status=HTTPStatusCode.OK)

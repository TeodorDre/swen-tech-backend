from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.platform.router.common import send_success_response


class SessionLogoutHandler(RouteHandler):
    path = '/session/logout'

    def __init__(self, log_service: LogService):
        super().__init__(log_service)

        self.path = SessionLogoutHandler.path
        self.request_type = hdrs.METH_POST

        self.name = 'client.session.logout'

    def handler(self, request: web.Request) -> web.Response:

        return send_success_response(self.name, 'OK')

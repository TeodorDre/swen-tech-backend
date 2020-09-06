from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService


class EchoRouteHandler(RouteHandler):
    def __init__(self, log_service: LogService):
        super().__init__(log_service)

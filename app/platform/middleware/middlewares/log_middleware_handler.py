from app.platform.middleware.middleware_handler import MiddlewareHandler
from app.platform.log.log_service import LogService
from aiohttp import web


class LogMiddlewareHandler(MiddlewareHandler):
    def __init__(self, log_service: LogService):
        super().__init__(log_service)

        self.routes = []

    async def call(self, request: web.Request, handler):
        self.log_service.info('LogMiddleware - request ' + request.match_info.route.name + 'called.')

        response = await handler(request)

        return response

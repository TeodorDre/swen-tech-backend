from app.platform.middleware.middleware_handler import MiddlewareHandler
from aiohttp import web


class SessionIdMiddleware(MiddlewareHandler):
    def __init__(self):
        super().__init__()

        self.routes = []

    async def call(self, request: web.Request, handler):
        response = await handler(request)

        return response

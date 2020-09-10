from app.platform.middleware.middleware_handler import MiddlewareHandler
from aiohttp import web


class SessionIdMiddleware(MiddlewareHandler):
    def __init__(self):
        super().__init__()

        self.routes = [
            'client.session.info',
            'client.session.logout'
        ]

    async def call(self, request_name: str, request: web.Request, handler):
        if request_name in self.routes:
            await self.handle(request)

        return await handler(request)

    async def handle(self, request: web.Request):
        body = await request.json()

        print(body)

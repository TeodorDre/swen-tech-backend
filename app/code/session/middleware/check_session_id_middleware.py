from app.platform.middleware.middleware_handler import MiddlewareHandler
from aiohttp import web
from app.base.errors import ValidationError

from app.platform.router.common import bad_request_response


class SessionIdMiddleware(MiddlewareHandler):
    def __init__(self):
        super().__init__()

        self.routes = [
            'client.session.info',
            'client.session.logout'
        ]

    async def call(self, request_name: str, request: web.Request, handler):
        if request_name in self.routes:
            try:
                await self.handle(request)
            except ValidationError as error:
                return bad_request_response(request_name, error.message)

        return await handler(request)

    async def handle(self, request: web.Request):
        body = await request.json()

        if 'sessionId' in body:
            return

        raise ValidationError('Field sessionId is required')

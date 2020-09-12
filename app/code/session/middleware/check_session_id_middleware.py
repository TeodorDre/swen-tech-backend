from app.platform.middleware.middleware_handler import MiddlewareHandler
from aiohttp import web
from app.base.errors import ValidationError
from app.db import users, sessions

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

    async def find_session(self, request: web.Request, session_id: str):
        async with request.app['db'].acquire() as connection:
            try:
                session = await connection.execute(
                    sessions.select().where(sessions.c.session_id == session_id)
                )

                if session.rowcount == 0:
                    return send_not_found_response(self.name, 'Session with id ' + session_id + ' was not found.')
            except Exception:
                return send_unexpected_error_response(self.name)

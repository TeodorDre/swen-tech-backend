from app.platform.middleware.middleware_handler import MiddlewareHandler
from aiohttp import web
from app.base.errors import ValidationError, DBRecordNotFoundError
from app.db import sessions

from app.platform.router.router_service import RouterService


class SessionIdMiddleware(MiddlewareHandler):
    def __init__(self, router_service: RouterService):
        super().__init__()

        self.router_service = router_service

        self.routes = [
            'client.session.info',
            'client.session.logout',
            'resources.tag.create'
        ]

    async def call(self, request_name: str, request: web.Request, handler):
        if request_name in self.routes:
            try:
                await self.handle(request)
            except (ValidationError, DBRecordNotFoundError) as error:
                if isinstance(error, ValidationError):
                    return self.router_service.send_bad_request_response(request_name, error.message)
                if isinstance(error, DBRecordNotFoundError):
                    return self.router_service.send_not_found_response(request_name, error.message)

        return await handler(request)

    async def handle(self, request: web.Request):
        body = await request.json()

        if 'sessionId' in body:
            session_id = body['sessionId']

            if isinstance(session_id , str):
                return await self.find_session(request, session_id )

            raise ValidationError('Field sessionId must be a string')
        else:
            raise ValidationError('Field sessionId is required')

    async def find_session(self, request: web.Request, session_id: str):
        async with request.app['db'].acquire() as connection:
            session = await connection.execute(
                sessions.select().where(sessions.c.session_id == session_id)
            )

            if session.rowcount == 0:
                raise DBRecordNotFoundError('Session with id ' + session_id + ' was not found.')

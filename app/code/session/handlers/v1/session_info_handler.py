from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.platform.router.common import send_success_response, send_unexpected_error_response, send_not_found_response

from app.db import sessions


class SessionInfoHandler(RouteHandler):
    path = '/session/info'

    def __init__(self, log_service: LogService):
        super().__init__(log_service)

        self.path = SessionInfoHandler.path
        self.request_type = hdrs.METH_POST

        self.name = 'client.session.info'

    async def handler(self, request: web.Request) -> web.Response:
        body = await request.json()

        session_id = body['sessionId']

        async with request.app['db'].acquire() as connection:
            try:
                session = await connection.execute(
                    sessions.select().where(sessions.c.session_id == session_id)
                )

                if session.rowcount == 0:
                    return send_not_found_response(self.name, 'Session with id ' + session_id + ' was not found.')
            except Exception:
                return send_unexpected_error_response(self.name)

        return send_success_response(self.name, 'OK')

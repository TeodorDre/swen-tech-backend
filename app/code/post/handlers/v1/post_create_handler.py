from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs

from app.platform.router.router_service import RouterService
from app.code.session.session_service import SessionService

from app.platform.database.database_service import DatabaseService
from jsonschema import validate, ValidationError as JSONValidationError
from psycopg2 import IntegrityError

from ...validation.post import CREATE_POST_SCHEMA


class PostCreateHandler(RouteHandler):
    path = '/post'

    def __init__(self, log_service: LogService, router_service: RouterService, session_service: SessionService,
                 database_service: DatabaseService):
        super().__init__(log_service)

        self.path = PostCreateHandler.path
        self.request_type = hdrs.METH_POST

        self.router_service = router_service
        self.session_service = session_service
        self.database_service = database_service

        self.name = 'resources.post.create'

    async def handler(self, request: web.Request) -> web.Response:
        body: dict = await request.json()

        session_id = body.pop('sessionId')

        try:
            validate(body, CREATE_POST_SCHEMA)

            return await self.do_handle(body, session_id)
        except JSONValidationError as error:
            return self.router_service.send_bad_request_response(self.name, error.message)

    async def do_handle(self, body: dict, session_id: str) -> web.Response:
        session: dict = await self.session_service.get_user_session_by_id(session_id)

        category = body.copy()
        category['client_id'] = session['client_id']

        try:
            pass
        except IntegrityError as error:
            return self.router_service.send_bad_request_response(self.name, error.pgerror)

from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs

from app.platform.router.common import send_success_response
from ...tag_service import TagService
from jsonschema import validate, ValidationError as JSONValidationError

from app.code.tag.validation.tag import CREATE_TAG_SCHEMA
from app.platform.router.router_service import RouterService
from app.code.session.session_service import SessionService

from app.platform.database.database_service import DatabaseService
from psycopg2 import IntegrityError


class TagCreateHandler(RouteHandler):
    path = '/tag'

    def __init__(self, log_service: LogService, tag_service: TagService, router_service: RouterService,
                 session_service: SessionService, database_service: DatabaseService):
        super().__init__(log_service)

        self.tag_service = tag_service
        self.router_service = router_service
        self.session_service = session_service
        self.database_service = database_service

        self.path = TagCreateHandler.path
        self.request_type = hdrs.METH_POST

        self.name = 'resources.tag.create'

    async def handler(self, request: web.Request) -> web.Response:
        body: dict = await request.json()

        session_id = body.pop('sessionId')

        try:
            validate(body, CREATE_TAG_SCHEMA)

            return await self.do_handle(body, session_id)
        except JSONValidationError as error:
            return self.router_service.send_bad_request_response(self.name, error.message)

    async def do_handle(self, body: dict, session_id: str) -> web.Response:
        session: dict = await self.session_service.get_user_session_by_id(session_id)

        tag = body.copy()
        tag['client_id'] = session['client_id']

        try:
            tag_result = await self.tag_service.create_tag(tag)

            return send_success_response(self.name, tag_result)
        except IntegrityError as error:
            return self.router_service.send_bad_request_response(self.name, error.pgerror)

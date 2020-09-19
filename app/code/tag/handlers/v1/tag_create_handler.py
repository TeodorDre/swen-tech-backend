from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs

from app.platform.router.common import send_success_response
from ...tag_service import TagService
from jsonschema import validate, ValidationError as JSONValidationError

from app.code.tag.validation.tag import CREATE_TAG_SCHEMA
from app.platform.router.router_service import RouterService
from app.code.session.session_service import SessionService

from app.db import tags, tags_lang

'''
# TAG_CREATE_STRUCT
{
  sessionId: string
  slug: string
  
  translations: [ru, en, fr]

}


'''


class TagCreateHandler(RouteHandler):
    path = '/tag'

    def __init__(self, log_service: LogService, tag_service: TagService, router_service: RouterService,
                 session_service: SessionService):
        super().__init__(log_service)

        self.tag_service = tag_service
        self.router_service = router_service
        self.session_service = session_service

        self.path = TagCreateHandler.path
        self.request_type = hdrs.METH_POST

        self.name = 'resources.tag.create'

    async def handler(self, request: web.Request) -> web.Response:
        body: dict = await request.json()

        session_id = body.pop('sessionId')

        try:
            validate(body, CREATE_TAG_SCHEMA)

            return await self.do_handle(request, body, session_id)
        except JSONValidationError as error:
            return self.router_service.send_bad_request_response(self.name, error.message)

    async def do_handle(self, request: web.Request, body: dict, session_id: str) -> web.Response:
        async with request.app['db'].acquire() as conn:
            try:
                result = await conn.execute(tags.insert().values(body))

                print(result)

                pass
            except Exception as e:
                pass
            return send_success_response(self.name, 'OK')

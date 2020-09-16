from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs

from app.platform.router.common import send_success_response
from ...tag_service import TagService
from jsonschema import validate, ValidationError as JSONValidationError

from app.code.tag.validation.tag import CREATE_TAG_SCHEMA
from app.platform.router.router_service import RouterService

'''
# TAG_CREATE_STRUCT
{
  sessionId: string
  slug: string
  
  nameRu: string
  nameEn: string
  nameFr: string

}


'''


class TagCreateHandler(RouteHandler):
    path = '/tag'

    def __init__(self, log_service: LogService, tag_service: TagService, router_service: RouterService):
        super().__init__(log_service)

        self.tag_service = tag_service
        self.router_service = router_service

        self.path = TagCreateHandler.path
        self.request_type = hdrs.METH_POST

        self.name = 'resources.tag.create'

    async def handler(self, request: web.Request) -> web.Response:
        body: dict = await request.json()

        session_id = body.pop('sessionId')

        print(body)

        try:
            validate(body, CREATE_TAG_SCHEMA)
        except JSONValidationError as error:
            return self.router_service.send_bad_request_response(self.name, error.message)

        return send_success_response(self.name, 'OK')

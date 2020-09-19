from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from app.platform.router.router_service import RouterService

from aiohttp import web, hdrs
from app.platform.router.common import send_success_response
from ...tag_service import TagService
from jsonschema import validate, ValidationError as JSONValidationError
from app.code.tag.validation.tag import DELETE_TAG_SCHEMA


class TagDeleteHandler(RouteHandler):
    path = '/tag'

    def __init__(self, log_service: LogService, router_service: RouterService, tag_service: TagService):
        super().__init__(log_service)

        self.tag_service = tag_service
        self.router_service = router_service

        self.path = TagDeleteHandler.path
        self.request_type = hdrs.METH_DELETE

        self.name = 'resources.tag.delete'

    async def handler(self, request: web.Request) -> web.Response:
        body: dict = await request.json()

        body.pop('sessionId')

        try:
            validate(body, DELETE_TAG_SCHEMA)

            return await self.do_handle(body)
        except JSONValidationError as error:
            return self.router_service.send_bad_request_response(self.name, error.message)

    async def do_handle(self, body: dict):
        try:
            await self.tag_service.delete_tag(body['id'])
        except Exception as error:
            pass

        return send_success_response(self.name, 'OK')

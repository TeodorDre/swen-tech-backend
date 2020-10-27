from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from jsonschema import validate, ValidationError as JSONValidationError
from psycopg2 import IntegrityError
from app.base.errors import DBRecordNotFoundError

from ...validation.post import DELETE_POST_SCHEMA

from app.platform.router.router_service import RouterService
from app.code.post.post_service import PostService


class PostDeleteHandler(RouteHandler):
    path = '/post/'

    def __init__(self, log_service: LogService, router_service: RouterService, post_service: PostService):
        super().__init__(log_service)

        self.path = PostDeleteHandler.path
        self.request_type = hdrs.METH_DELETE

        self.router_service = router_service
        self.post_service = post_service

        self.name = 'resources.post.delete'

    async def handler(self, request: web.Request) -> web.Response:
        body: dict = await request.json()

        body.pop('sessionId')

        try:
            validate(body, DELETE_POST_SCHEMA)

            return await self.do_handle(body)
        except JSONValidationError as error:
            return self.router_service.send_bad_request_response(self.name, error.message)

    async def do_handle(self, body: dict):
        post_id: int = body['id']

        try:
            await self.post_service.delete_post(post_id)

            return self.router_service.send_success_response(self.name, 'OK')
        except IntegrityError as error:
            return self.router_service.send_bad_request_response(self.name, error.pgerror)
        except DBRecordNotFoundError as error:
            return self.router_service.send_not_found_response(self.name, error.message)

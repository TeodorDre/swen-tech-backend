from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs

from app.platform.router.router_service import RouterService
from app.code.post.post_service import PostService


class PostGetAllHandler(RouteHandler):
    path = '/post/'

    def __init__(self, log_service: LogService, router_service: RouterService, post_service: PostService):
        super().__init__(log_service)

        self.path = PostGetAllHandler.path
        self.request_type = hdrs.METH_GET

        self.router_service = router_service
        self.post_service = post_service

        self.name = 'resources.post.get_all'

    async def handler(self, request: web.Request) -> web.Response:
        lang = request.get('lang')

        try:
            posts = await self.post_service.get_all(lang)

            return self.router_service.send_success_response(self.name, posts)
        except Exception as error:
            return self.router_service.send_unexpected_error_response(self.name, error)


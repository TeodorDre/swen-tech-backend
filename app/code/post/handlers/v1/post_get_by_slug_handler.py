from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs

from app.base.errors import DBRecordNotFoundError

from app.platform.router.router_service import RouterService
from app.code.post.post_service import PostService


class PostGetBySlugHandler(RouteHandler):
    path = '/post/{slug}'

    def __init__(self, log_service: LogService, router_service: RouterService, post_service: PostService):
        super().__init__(log_service)

        self.path = PostGetBySlugHandler.path
        self.request_type = hdrs.METH_GET

        self.router_service = router_service
        self.post_service = post_service

        self.name = 'resources.post.get_by_slug'

    async def handler(self, request: web.Request) -> web.Response:
        post_slug: str = request.match_info['slug']

        lang = request.get('lang')

        try:
            post = await self.post_service.get_post_by_slug(post_slug, lang)

            return self.router_service.send_success_response(self.name, post)
        except DBRecordNotFoundError as error:
            return self.router_service.send_not_found_response(self.name, error.message)

    async def do_handle(self, session_result, conn) -> web.Response:
        pass

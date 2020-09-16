from app.platform.router.router_handler import RouteHandler
from app.platform.log.log_service import LogService
from aiohttp import web, hdrs
from app.platform.router.common import send_success_response
from ...tag_service import TagService

'''
# TAG_CREATE_STRUCT
{
  authorId: number
  tagSlug: string
  
  nameRu: string
  nameEn: string
  nameFr: string

}


'''


class TagCreateHandler(RouteHandler):
    path = '/tag'

    def __init__(self, log_service: LogService, tag_service: TagService):
        super().__init__(log_service)

        self.tag_service = tag_service

        self.path = TagCreateHandler.path
        self.request_type = hdrs.METH_POST

        self.name = 'resources.tag.create'

    async def handler(self, request: web.Request) -> web.Response:
        body = await request.json()

        print(body)

        return send_success_response(self.name, 'OK')

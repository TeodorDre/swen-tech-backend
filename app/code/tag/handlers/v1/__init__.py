from .tag_update_handler import TagUpdateHandler
from .tag_create_handler import TagCreateHandler
from .tag_get_all_handler import TagGetAllHandler
from .tag_delete_handler import TagDeleteHandler

__all__ = ['tag_routes']

tag_routes = [TagGetAllHandler, TagDeleteHandler, TagCreateHandler, TagUpdateHandler]

for route in tag_routes:
    route.path = '/v1' + route.path

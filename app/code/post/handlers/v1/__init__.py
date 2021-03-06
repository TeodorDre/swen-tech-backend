from .post_update_handler import PostUpdateHandler
from .post_create_handler import PostCreateHandler
from .post_get_all_handler import PostGetAllHandler
from .post_delete_handler import PostDeleteHandler
from .post_get_by_slug_handler import PostGetBySlugHandler

__all__ = ['post_routes']

post_routes = [PostGetAllHandler, PostDeleteHandler, PostCreateHandler, PostUpdateHandler, PostGetBySlugHandler]

for route in post_routes:
    route.path = '/v1' + route.path

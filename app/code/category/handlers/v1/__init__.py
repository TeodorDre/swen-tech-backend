from app.code.category.handlers.v1.category_create_handler import CategoryCreateHandler
from app.code.category.handlers.v1.category_delete_handler import CategoryDeleteHandler
from app.code.category.handlers.v1.category_get_all_handler import CategoryGetAllHandler
from app.code.category.handlers.v1.category_update_handler import CategoryUpdateHandler

__all__ = ['category_routes']

category_routes = [CategoryCreateHandler, CategoryDeleteHandler, CategoryGetAllHandler, CategoryUpdateHandler]

for route in category_routes:
    route.path = '/v1' + route.path

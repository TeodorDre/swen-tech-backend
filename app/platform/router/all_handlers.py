from app.code.session.handlers.v1 import session_routes
from app.code.category.handlers.v1 import category_routes

__all__ = ['all_routes']

all_routes = \
    [
        *session_routes,
        *category_routes
    ]

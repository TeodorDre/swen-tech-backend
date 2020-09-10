from aiohttp import web
from app.base.database import init_pg, close_pg
from configuration import DB_CONFIG
import aiohttp_cors

from app.main import instantiation_service
from app.platform.router.router_service import RouterService

from app.platform.router.handlers.echo_handler import EchoRouteHandler
from app.platform.router.handlers.variable_handler import VariableRouteHandler
from app.platform.router.router_handler import RouteHandler

from typing import List
from app.platform.router.all_handlers import all_routes

from app.platform.middleware.middleware_service import MiddlewareService
from app.platform.middleware.middlewares.log_middleware_middleware import LogMiddleware
from app.platform.middleware.middleware_handler import MiddlewareHandler
from app.platform.middleware.middlewares.json_response_type_middleware import JSONResponseTypeMiddleware
from app.code.middleware import all_middlewares


def middleware_factory(middleware):
    @web.middleware
    async def middleware_call(request, handler):
        request_name = request.match_info.route.name

        return await middleware(request_name, request, handler)

    return middleware_call


def create_app():
    # setup routes
    router_service: RouterService = instantiation_service.invoke_function(
        lambda accessor: accessor.get('router_service'))

    router_service.add_route_handler(EchoRouteHandler)
    router_service.add_route_handler(VariableRouteHandler)

    for route in all_routes:
        if issubclass(route, RouteHandler):
            router_service.add_route_handler(route)

    # setup middleware
    middleware_service: MiddlewareService = instantiation_service.invoke_function(
        lambda accessor: accessor.get('middleware_service')
    )

    middleware_service.register_middleware(LogMiddleware)
    middleware_service.register_middleware(JSONResponseTypeMiddleware)

    for middleware in all_middlewares:
        if issubclass(middleware, MiddlewareHandler):
            middleware_service.register_middleware(middleware)

    middlewares = map(lambda middleware_item: middleware_factory(middleware_item.call), middleware_service.middlewares)

    # create application
    app = web.Application(middlewares=middlewares)

    # setup configuration
    app['config'] = DB_CONFIG

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    # setup views and router
    setup_routes(app, router_service.routes)

    # add cors
    for route in list(app.router.routes()):
        cors.add(route)

    # create db connection on startup, shutdown on exit
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

    return app


def setup_routes(app, routes: List[RouteHandler]):
    for route in routes:
        app.router.add_route(route.request_type, route.path, route.handler, name=route.name)

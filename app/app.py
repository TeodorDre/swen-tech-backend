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
from app.platform.middleware.middlewares.log_middleware_handler import LogMiddlewareHandler


def create_app():
    router_service: RouterService = instantiation_service.invoke_function(
        lambda accessor: accessor.get('router_service'))

    router_service.add_route_handler(EchoRouteHandler)
    router_service.add_route_handler(VariableRouteHandler)

    for route in all_routes:
        router_service.add_route_handler(route)

    middleware_service: MiddlewareService = instantiation_service.invoke_function(
        lambda accessor: accessor.get('middleware_service')
    )

    middleware_service.register_middleware(LogMiddlewareHandler)

    middlewares = map(lambda middleware: middleware.call, middleware_service.middlewares)

    def middleware_factory(middleware):
        @web.middleware
        async def middleware_call(request, handler):
            return await middleware(request, handler)

        return middleware_call

    factory_middlewares = map(middleware_factory, middlewares)

    app = web.Application(middlewares=factory_middlewares)

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

    for route in list(app.router.routes()):
        cors.add(route)

    # create db connection on startup, shutdown on exit
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)

    return app


def setup_routes(app, routes: List[RouteHandler]):
    for route in routes:
        app.router.add_route(route.request_type, route.path, route.handler, name=route.name)

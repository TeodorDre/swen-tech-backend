from aiohttp import web
from app.base.database import init_pg, close_pg
from configuration import DB_CONFIG
import aiohttp_cors

from app.main import instantiation_service
from app.platform.instantiation.instantiation_service import Accessor
from app.platform.log.log_service import LogService

from app.platform.router.router_service import RouterService

from app.platform.router.handlers.echo_handler import EchoRouteHandler
from app.platform.router.handlers.variable_handler import VariableRouteHandler
from app.platform.router.router_handler import RouteHandler
from typing import List


def create_app():
    app = web.Application(middlewares=[])
    # setup configuration
    app['config'] = DB_CONFIG

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    def get_log_service(accessor: Accessor) -> LogService:
        return accessor.get('log_service')

    log_service: LogService = instantiation_service.invoke_function(get_log_service)
    log_service.info('Hello from log_service')

    router_service: RouterService = instantiation_service.invoke_function(
        lambda accessor: accessor.get('router_service'))

    router_service.add_route_handler(EchoRouteHandler)
    router_service.add_route_handler(VariableRouteHandler)

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
        app.router.add_route(route.request_type, route.path, route.handler)

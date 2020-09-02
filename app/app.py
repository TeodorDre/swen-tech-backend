from aiohttp import web
from app.routes import setup_routes
from app.base.database import init_pg, close_pg
from configuration import DB_CONFIG
import aiohttp_cors

from app.main import instantiationService
from app.platform.instantiation.instantiation_service import Accessor


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

    def get_log_service(accessor: Accessor):
        log_service = accessor.get('log_service')

        print(log_service)

    instantiationService.invoke_function(get_log_service)

    # setup views and router
    setup_routes(app)

    for route in list(app.router.routes()):
        cors.add(route)

    # create db connection on startup, shutdown on exit
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)
    return app

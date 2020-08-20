from aiohttp import web
from app.routes import setup_routes
from app.utils import init_pg, close_pg
from configuration import DB_CONFIG
from app.middlewares import json_checker
import aiohttp_cors


def create_app():
    app = web.Application(middlewares=[json_checker])
    # setup configuration
    app['config'] = DB_CONFIG

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    # setup views and routes
    setup_routes(app)

    for route in list(app.router.routes()):
        cors.add(route)

    # create db connection on startup, shutdown on exit
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)
    return app

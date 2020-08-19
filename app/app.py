from aiohttp import web
from app.routes import setup_routes
from app.utils import init_pg, close_pg
from configuration import DB_CONFIG
from app.middlewares import json_checker


def create_app():
    app = web.Application(middlewares=[json_checker])
    # setup configuration
    app['config'] = DB_CONFIG

    # setup views and routes
    setup_routes(app)

    # create db connection on startup, shutdown on exit
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)
    return app

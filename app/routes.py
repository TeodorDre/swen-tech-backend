from app.handlers import *


def setup_routes(app):
    app.router.add_get('/echo', echo)
    app.router.add_get('/{name}', variable_handler)

    # Andrew Slesarenko (swen295@gmail.com)

    # User routes

    app.router.add_post('/api/v1/session/login', session_login, name='session_login')
    app.router.add_post('/api/v1/session/logout', session_logout, name='session_logout')
    app.router.add_post('/api/v1/session/info', session_info, name='session_info')

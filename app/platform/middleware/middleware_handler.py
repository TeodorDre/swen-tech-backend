from ..instantiation.disposable import Disposable
from aiohttp import web


class MiddlewareHandler(Disposable):
    def __init__(self):
        pass

    def call(self, request: web.Request, handler):
        pass

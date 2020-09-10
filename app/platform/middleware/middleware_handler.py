from ..instantiation.disposable import Disposable
from ..log.log_service import LogService
from aiohttp import web


class MiddlewareHandler(Disposable):
    def __init__(self, log_service: LogService):
        self.log_service = log_service

    def call(self, request: web.Request, handler):
        pass

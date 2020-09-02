from app.platform.instantiation.disposable import Disposable
from aiohttp import web
from app.platform.log.log_service import LogService


class RouterHandler(Disposable):
    def __init__(self, log_service: LogService):
        self.log_service = log_service


    def use(self, request) -> web.Response:
        self.log_service.info('Request received')

from app.platform.instantiation.disposable import Disposable
from app.platform.log.log_service import LogService


class RouteHandler(Disposable):
    def __init__(self, log_service: LogService):
        self.log_service = log_service

        self.path = ''
        self.request_type = ''

    def handler(self):
        pass

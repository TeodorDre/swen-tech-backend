from ..instantiation.disposable import Disposable
from ..log.log_service import LogService



class MiddlewareHandler(Disposable):
    def __init__(self, log_service: LogService):
        self.log_service = log_service

    def call(self, request, handler):

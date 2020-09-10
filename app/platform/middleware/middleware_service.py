from ..instantiation.disposable import Disposable
from ..instantiation.instantiation_service import InstantiationService
from ..lifecycle.lifecycle_service import LifecycleService
from ..middleware.middleware_handler import MiddlewareHandler


class MiddlewareService(Disposable):
    def __init__(self, lifecycle_service: LifecycleService, instantiation_service: InstantiationService):
        self.lifecycle_service = lifecycle_service
        self.instantiation_service = instantiation_service
        self.middlewares = dict()

    def register_middleware(self, name: str, middleware: MiddlewareHandler):
        self.middlewares[name] = middleware

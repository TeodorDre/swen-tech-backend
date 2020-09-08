from app.platform.instantiation.disposable import Disposable
from app.platform.instantiation.instantiation_service import InstantiationService

from app.platform.log.log_service import LogService
from app.platform.lifecycle.lifecycle_service import LifecycleService


class RouterService(Disposable):
    def __init__(self, log_service: LogService,
                 lifecycle_service: LifecycleService,
                 instantiation_service: InstantiationService):
        self.log_service = log_service
        self.lifecycle_service = lifecycle_service
        self.instantiation_service = instantiation_service

        self.routes = []

    def add_route_handler(self, route_handler):
        route_instance = self.instantiation_service.create_instance(route_handler)

        self.routes.append(route_instance)

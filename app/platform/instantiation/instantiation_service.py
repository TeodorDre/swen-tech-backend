from app.platform.instantiation.service_collection import ServiceCollection
from app.platform.instantiation.disposable import Disposable
from app.base.errors import ApplicationError

__all__ = ['InstantiationService', 'Accessor']


class InstantiationError(ApplicationError):
    pass


class Accessor(Disposable):
    def __init__(self, services: ServiceCollection, is_done: bool = True):
        self.services = services
        self.done = is_done

    def get(self, identifier: str):
        if not self.done:
            print('Service accessor is only valid during the invocation of its target method')

        instance = self.services.get(identifier)

        if not instance:
            raise InstantiationError('[invokeFunction] unknown service ' + identifier)

        return instance


class InstantiationService:
    def __init__(self, services: ServiceCollection):
        self.services = services

    def invoke_function(self, fn):
        _done = False

        try:
            accessor = Accessor(self.services, _done)

            return fn(accessor)
        finally:
            _done = True
from app.platform.instantiation.disposable import Disposable


class ServiceCollection(Disposable):
    def __init__(self, strict=False):
        self.strict = strict

        self.services = {}

    def set(self, id, service):
        self.services[id] = service

    def get(self, id):
        return self.services.get(id)

from app.platform.instantiation.service_collection import ServiceCollection
from app.platform.instantiation.instantiation_service import InstantiationService

from app.platform.log.log_service import LogService, LogLevel

__all__ = ['instantiationService']

# Создаем коллекцию сервисов
services = ServiceCollection()

# Создаем основной инстанцирующий сервис
instantiationService = InstantiationService(services)

# log service
logService = LogService(LogLevel.Info)
services.set('log_service', logService)

from app.platform.instantiation.disposable import Disposable
from app.platform.database.database_service import DatabaseService


class TagService(Disposable):
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def create_tag(self):
        pass

    async def delete_tag(self):
        pass

    async def update_tag(self):
        pass

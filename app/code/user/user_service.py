from app.platform.instantiation.disposable import Disposable
from app.platform.database.database_service import DatabaseService
from app.base.errors import DBRecordNotFoundError
from app.db import users


class UserService(Disposable):
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def create_user(self, user: dict):
        print(user)

    async def update_user(self):
        pass

    async def delete_user(self):
        pass

    async def get_user(self):
        pass

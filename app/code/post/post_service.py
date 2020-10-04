from app.platform.instantiation.disposable import Disposable
from app.platform.database.database_service import DatabaseService
from app.db import posts, posts_lang
from sqlalchemy import sql
from app.base.errors import DBRecordNotFoundError


class PostService(Disposable):
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def create_post(self, post: dict):
        print(post)

        pass

    async def delete_post(self):
        pass

    async def update_post(self):
        pass

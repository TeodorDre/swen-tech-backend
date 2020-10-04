from app.platform.instantiation.disposable import Disposable
from app.platform.database.database_service import DatabaseService
from app.db import posts, posts_lang
from sqlalchemy import sql
from app.base.errors import DBRecordNotFoundError
from enum import Enum


class PostPublishedStatus(Enum):
    NotPublished = 1,


class PostService(Disposable):
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def create_post(self, post: dict):
        async with self.database_service.instance.acquire() as conn:
            url = post.get('title')

            tags: list = post.get('tags')

            formatted_post = {
                'client_id': post.get('client_id'),
                'post_slug': post.get('slug'),
                'post_url': url,
                'post_featured_image': post.get('poster'),
                'post_status': PostPublishedStatus.NotPublished.value[0],
                'post_tags_id': tags,
            }

            # await conn.execute(posts.insert().values(formatted_post))

    async def delete_post(self):
        pass

    async def update_post(self):
        pass

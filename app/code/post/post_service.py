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

    async def get_post_by_slug(self, slug: str):
        async with self.database_service.instance.acquire() as connection:
            post_result = await connection.execute(
                posts.select().where(posts.c.post_slug == slug)
            )

            if post_result.rowcount == 0:
                raise DBRecordNotFoundError('Post with slug ' + slug + ' was not found')

            return await self.do_get_post_by_slug(post_result)

    async def do_get_post_by_slug(self, post_result):
        for post in post_result:
            post = dict(post)

            print(post)

    async def create_post(self, post: dict):
        async with self.database_service.instance.acquire() as conn:
            title: list = post.get('title')
            texts: list = post.get('body')

            ru_title = title[0]
            en_title = title[1]
            fr_title = title[2]

            ru_text = texts[0]
            en_text = texts[1]
            fr_text = texts[2]

            slug = post.get('slug')
            poster = post.get('poster')

            tags: list = post.get('tags')

            if not tags:
                tags = []

            post_category_id = post.get('category')

            formatted_post = {
                'client_id': post.get('client_id'),
                'post_slug': slug,
                'post_url': slug,
                'post_featured_image': poster,
                'post_status': 1,
                'post_tags_id': tags,
                'category_id': post_category_id,
            }

            await conn.execute(posts.insert().values(formatted_post))

            result = await conn.execute(
                sql.select([sql.func.max(posts.c.post_id).label('post_id')])
            )

            post = await result.fetchone()
            formatted_post: dict = dict(post)

            post_id = formatted_post.get('post_id')

            post_translation = {
                'post_id': post_id,

                'text_ru': ru_text,
                'text_en': en_text,
                'text_fr': fr_text,

                'title_ru': ru_title,
                'title_en': en_title,
                'title_fr': fr_title
            }

            await conn.execute(posts_lang.insert().values(post_translation))

            return formatted_post

    async def delete_post(self, post_id: int):
        async with self.database_service.instance.acquire() as conn:
            result = await conn.execute(posts.delete().where(posts.c.post_id == post_id))

            if result.rowcount == 0:
                raise DBRecordNotFoundError('Tag with id ' + str(post_id) + ' was not found.')

    async def update_post(self):
        pass

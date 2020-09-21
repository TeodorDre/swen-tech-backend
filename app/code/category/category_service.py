from app.platform.instantiation.disposable import Disposable
from app.platform.database.database_service import DatabaseService
from app.db import categories, categories_lang
from sqlalchemy import sql
from app.base.errors import DBRecordNotFoundError


class CategoryService(Disposable):
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def create_category(self, tag: dict):
        async with self.database_service.instance.acquire() as conn:
            translations: list = tag.get('translations')

            ru_translation = translations[0]
            en_translation = translations[1]
            fr_translation = translations[2]

            formatted_tag = {
                'tag_slug': tag['slug'],
                'client_id': tag['client_id']
            }

            await conn.execute(tags.insert().values(formatted_tag))

            result = await conn.execute(
                sql.select([sql.func.max(tags.c.tag_id).label('tag_id')])
            )

            tag = await result.fetchone()
            formatted_tag: dict = dict(tag)
            tag_id = formatted_tag.get('tag_id')

            tag_translation = {
                'name_ru': ru_translation,
                'name_en': en_translation,
                'name_fr': fr_translation,
                'tag_id': tag_id
            }

            await conn.execute(tags_lang.insert().values(tag_translation))

            return formatted_tag

    async def delete_category(self, tag_id: int):
        async with self.database_service.instance.acquire() as conn:
            result = await conn.execute(tags.delete().where(tags.c.tag_id == tag_id))

            if result.rowcount == 0:
                raise DBRecordNotFoundError('Tag with id ' + str(tag_id) + ' was not found.')

    async def update_category(self):
        pass

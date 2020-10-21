from app.platform.instantiation.disposable import Disposable
from app.platform.database.database_service import DatabaseService
from app.db import categories, categories_lang
from sqlalchemy import sql
from app.base.errors import DBRecordNotFoundError


class CategoryService(Disposable):
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def get_category_by_id(self, category_id: int):
        async with self.database_service.instance.acquire() as conn:
            category_result = await conn.execute(categories.select().where(categories.c.category_id == category_id))

            if category_result.rowcount == 0:
                return None

            for category in category_result:
                category = dict(category)

                category_lang_result = await conn.execute(
                    categories_lang.select().where(categories_lang.c.category_id == category_id))

                for category_lang in category_lang_result:
                    category_lang = dict(category_lang)

                    return {
                        'lang': category_lang,
                        'data': category,
                    }

    async def create_category(self, category: dict):
        async with self.database_service.instance.acquire() as conn:
            translations: list = category.get('translations')

            ru_translation = translations[0]
            en_translation = translations[1]
            fr_translation = translations[2]

            formatted_category = {
                'category_slug': category['slug'],
                'client_id': category['client_id']
            }

            await conn.execute(categories.insert().values(formatted_category))

            result = await conn.execute(
                sql.select([sql.func.max(categories.c.category_id).label('category_id')])
            )

            category = await result.fetchone()
            formatted_category: dict = dict(category)
            category_id = formatted_category.get('category_id')

            category_translation = {
                'name_ru': ru_translation,
                'name_en': en_translation,
                'name_fr': fr_translation,
                'category_id': category_id
            }

            await conn.execute(categories_lang.insert().values(category_translation))

            return formatted_category

    async def delete_category(self, category_id: int):
        async with self.database_service.instance.acquire() as conn:
            result = await conn.execute(categories.delete().where(categories.c.category_id == category_id))

            if result.rowcount == 0:
                raise DBRecordNotFoundError('Tag with id ' + str(category_id) + ' was not found.')

    async def update_category(self):
        pass

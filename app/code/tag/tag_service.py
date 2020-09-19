from app.platform.instantiation.disposable import Disposable
from app.platform.database.database_service import DatabaseService
from app.db import tags, tags_lang
from sqlalchemy import sql


class TagService(Disposable):
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def create_tag(self, tag: dict):
        async with self.database_service.instance.acquire() as conn:
            translations: list = tag.get('translations')

            ru_translation = translations[0]
            en_translation = translations[1]
            fr_translation = translations[2]

            formatted_tag = {
                'tag_slug': tag['slug'],
                'created_by': tag['client_id']
            }

            await conn.execute(tags.insert().values(formatted_tag))

            result = await conn.execute(
                sql.select([sql.func.max(tags.c.tag_id).label('tag_id')])
            )

            print(result)

    async def delete_tag(self):
        pass

    async def update_tag(self):
        pass

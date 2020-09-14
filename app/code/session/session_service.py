from app.platform.instantiation.disposable import Disposable
from aiohttp import web
from app.db import users


class SessionService(Disposable):
    def __init__(self):
        pass

    async def get_user_session_by_email(self, request: web.Request, user_email: str):
        async with request.app['db'].acquire() as conn:
            result = await conn.execute(users.select().where(users.c.client_email == user_email))

            if result.rowcount == 0:
                return None

            for user in result:
                user = dict(user)

                return user

    async def login_user(self, request: web.Request, user) -> web.Response:
        print(user)

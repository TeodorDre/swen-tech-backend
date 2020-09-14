from app.platform.instantiation.disposable import Disposable
from aiohttp import web
from app.db import users
from app.base.errors import AuthenticatedError, AuthErrorCode


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

    async def login_user(self, request: web.Request, user: dict) -> web.Response:
        body = await request.json()

        request_password = body['password']
        user_password = user.get('password')

        if user_password != request_password:
            raise AuthenticatedError('', AuthErrorCode.InvalidPassword)

        user.pop('password', None)
        user.pop('created_ts', None)
        user.pop('updated_ts', None)

        print(user)

from app.platform.instantiation.disposable import Disposable
from aiohttp import web
from app.db import users, sessions
from app.base.errors import AuthenticatedError, AuthErrorCode
from app.base.uuid import generate_id


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

    async def login_user(self, request: web.Request, user: dict):
        body = await request.json()

        request_password = body['password']
        user_password = user.get('password')

        if user_password != request_password:
            raise AuthenticatedError('', AuthErrorCode.InvalidPassword)

        user.pop('password', None)
        user.pop('created_ts', None)
        user.pop('updated_ts', None)

        return await self.process_user_session(request, user)

    async def process_user_session(self, request: web.Request, user: dict):
        user_client_id = user['client_id']

        async with request.app['db'].acquire() as conn:
            has_session_result = await conn.execute(sessions.select().where(sessions.c.client_id == user_client_id))

            if has_session_result.rowcount == 0:
                session_id = generate_id(45)

                await conn.execute(sessions.insert().values({
                    'session_id': session_id,
                    'client_id': user_client_id
                }))

                create_session_result = await conn.execute(
                    sessions.select().where(sessions.c.client_id == user_client_id))

                if create_session_result.rowcount > 0:
                    for session in create_session_result:
                        session = dict(session)

                        return session
            else:
                for session in has_session_result:
                    session = dict(session)

                    return session

    def transform_session(self, session, user):
        new_session = dict()
        new_session['clientId'] = session['client_id']
        new_session['sessionId'] = session['session_id']

        profile = dict()

        profile['name'] = user['client_name']
        profile['email'] = user['client_email']

        new_session['profile'] = profile

        return new_session
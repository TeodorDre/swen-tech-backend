from app.db import users, sessions
from aiohttp import web
from app.code.session.session import process_user_session, transform_session
import logging

from app.base.network import HTTPStatusCode

__all__ = [
    'session_login', 'session_info', 'session_logout',
]


async def session_login(request) -> web.Response:
    body = await request.json()

    user_email = body['email']
    user_password = body['password']

    try:
        async with request.app['db'].acquire() as conn:
            result = await conn.execute(users.select().where(users.c.client_email == user_email))

            if result.rowcount == 0:
                return send_not_found_response()

            for user in result:
                user = dict(user)

                if user['password'] != user_password:
                    return send_not_found_response()

                user.pop('password', None)
                user.pop('created_ts', None)
                user.pop('updated_ts', None)

                session = await process_user_session(request, user)

                return web.json_response({
                    'result': 'success',
                    'session': transform_session(session, user)
                }, status=HTTPStatusCode.OK)

    except Exception as e:
        logging.error(e)

        return send_unexpected_error_response()


async def session_logout(request) -> web.Response:
    body = await request.json()

    session_id = body['sessionId']

    async with request.app['db'].acquire() as conn:
        try:
            result = await conn.execute(sessions.delete().where(sessions.c.session_id == session_id))
            if result.rowcount == 0:
                return send_not_found_response()
            return web.json_response(status=204)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')

            return send_unexpected_error_response()


async def session_info(request) -> web.Response:
    body = await request.json()

    session_id = body['sessionId']

    async with request.app['db'].acquire() as conn:
        try:
            session_result = await conn.execute(sessions.select().where(sessions.c.session_id == session_id))

            if session_result.rowcount == 0:
                return send_not_found_response()

            else:
                for session in session_result:
                    session = dict(session)

                    client_id = session['client_id']

                    user_result = await conn.execute(users.select().where(users.c.client_id == client_id))

                    for user in user_result:
                        user = dict(user)

                        return web.json_response({
                            'result': 'success',
                            'session': transform_session(session, user)
                        }, status=HTTPStatusCode.OK)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return send_unexpected_error_response()

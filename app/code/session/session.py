from app.db import sessions
from app.base.uuid import generate_id


async def process_user_session(request, user):
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
                    print(session)

                    session = dict(session)

                    return session
        else:
            print(has_session_result)

            for session in has_session_result:
                session = dict(session)

                return session


def transform_session(session, user):
    new_session = dict()
    new_session['clientId'] = session['client_id']
    new_session['sessionId'] = session['session_id']

    profile = dict()

    profile['name'] = user['client_name']
    profile['email'] = user['client_email']

    new_session['profile'] = profile

    return new_session

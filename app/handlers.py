from aiohttp import web
from sqlalchemy import sql
from psycopg2 import IntegrityError
from datetime import datetime
import logging

__all__ = [
    'echo', 'variable_handler',
]


async def echo(request) -> web.Response:
    return web.json_response({'status': 'OK'}, status=OK)


async def variable_handler(request) -> web.Response:
    return web.json_response({'error': f"Path: '{request.match_info['name']}' does't available"}, status=NOT_FOUND)


async def dataset_post(request, body) -> web.Response:
    async with request.app['db'].acquire() as conn:
        try:
            await conn.execute(datasets.insert().values(body))
        except IntegrityError as e:
            logging.error(f'IntegrityError: {e}')
            return web.json_response({'error': 'IntegrityError'}, status=INTERNAL_SERVER_ERROR)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)

        result = await conn.execute(
            sql.select([sql.func.max(datasets.c.dataset_id).label('dataset_id')])
        )
        new_id = await result.fetchone()
    return web.json_response({'message': f"Created with dataset id: {str(dict(new_id)['dataset_id'])}"},
                             status=CREATED)


async def dataset_get(request, body) -> web.Response:
    project_id = body['project_id']
    try:
        async with request.app['db'].acquire() as conn:
            records = []
            async for record in conn.execute(
                    datasets.select().where(datasets.c.project_id == project_id).order_by(datasets.c.dataset_id)):
                record = dict(record)
                record['created_ts'] = dt_converter(record['created_ts'])
                record['updated_ts'] = dt_converter(record['updated_ts'])
                records.append(record)
            if not records:
                return web.json_response({'error': f'Datasets for project: {project_id} not found'}, status=NOT_FOUND)

            return web.json_response(data=records)
    except Exception as e:
        logging.error(f'Unexpected Error: {e}')
        return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)


async def dataset_update(request, body) -> web.Response:
    dataset_id = body['dataset_id']
    body['updated_ts'] = datetime.utcnow()
    async with request.app['db'].acquire() as conn:
        try:
            result = await conn.execute(datasets.update().where(datasets.c.dataset_id == dataset_id).values(body))
            if result.rowcount == 0:
                return web.json_response({'error': f'Dataset with id: {dataset_id} not found'}, status=NOT_FOUND)
            return web.json_response({'message': f'Dataset with id: {dataset_id} is updated'}, status=OK)
        except IntegrityError as e:
            logging.error(f'IntegrityError: {e}')
            return web.json_response({'error': 'IntegrityError'}, status=INTERNAL_SERVER_ERROR)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)


async def dataset_delete(request, body) -> web.Response:
    dataset_id = body['dataset_id']
    async with request.app['db'].acquire() as conn:
        try:
            result = await conn.execute(datasets.delete().where(datasets.c.dataset_id == dataset_id))
            if result.rowcount == 0:
                return web.json_response({'error': f'Dataset with id: {dataset_id}  not found'}, status=NOT_FOUND)
            return web.json_response(status=204)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)

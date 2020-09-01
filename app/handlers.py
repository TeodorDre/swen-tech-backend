from aiohttp import web
from app.db import users, sessions, categories, categories_lang, tags, tags_lang, posts, posts_lang
from app.statuscodes import *
from app.utils import dt_converter, send_unexpected_error_response, send_not_found_response
from sqlalchemy import sql
from psycopg2 import IntegrityError
from datetime import datetime
import json
import logging

__all__ = [
    'echo', 'variable_handler',
]


async def echo(request) -> web.Response:
    return web.json_response({'status': 'OK'}, status=OK)


async def variable_handler(request) -> web.Response:
    return web.json_response({'error': f"Path: '{request.match_info['name']}' does't available"}, status=NOT_FOUND)


async def project_post(request, body) -> web.Response:
    async with request.app['db'].acquire() as conn:
        try:
            await conn.execute(projects.insert().values(body))
        except IntegrityError as e:
            logging.error(f'IntegrityError: {e}')
            return web.json_response({'error': 'IntegrityError'}, status=INTERNAL_SERVER_ERROR)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)

        result = await conn.execute(
            sql.select([sql.func.max(projects.c.project_id).label('project_id')])
        )
        new_id = await result.fetchone()
    return web.json_response({'message': f"Created with project id: {str(dict(new_id)['project_id'])}"},
                             status=CREATED)


async def project_get(request) -> web.Response:
    try:
        async with request.app['db'].acquire() as conn:
            records = []
            async for record in conn.execute(projects.select().order_by(projects.c.project_id)):
                if not record:
                    return web.json_response({'error': 'no projects yet'}, status=NOT_FOUND)
                record = dict(record)
                record['created_ts'] = dt_converter(record['created_ts'])
                record['updated_ts'] = dt_converter(record['updated_ts'])
                records.append(record)
            if not records:
                return web.json_response({'error': 'projects not found'}, status=NOT_FOUND)
            return web.json_response(data=records)
    except Exception as e:
        logging.error(f'Unexpected Error: {e}')
        return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)


async def project_update(request, body) -> web.Response:
    project_id = body['project_id']
    body['updated_ts'] = datetime.utcnow()
    async with request.app['db'].acquire() as conn:
        try:
            result = await conn.execute(projects.update().where(projects.c.project_id == project_id).values(body))
            if result.rowcount == 0:
                return web.json_response({'error': 'Project not found'}, status=NOT_FOUND)
            return web.json_response({'message': f'Project with id: {project_id} is updated'}, status=OK)
        except IntegrityError as e:
            logging.error(f'IntegrityError: {e}')
            return web.json_response({'error': 'IntegrityError'}, status=INTERNAL_SERVER_ERROR)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)


async def project_delete(request, body) -> web.Response:
    project_id = body['project_id']
    async with request.app['db'].acquire() as conn:
        try:
            result = await conn.execute(projects.delete().where(projects.c.project_id == project_id))
            if result.rowcount == 0:
                return web.json_response({'error': f'Project with id: {project_id} not found'}, status=NOT_FOUND)
            return web.json_response(status=204)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)


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


async def image_post(request, body) -> web.Response:
    async with request.app['db'].acquire() as conn:
        try:
            await conn.execute(images.insert().values(body))
        except IntegrityError as e:
            logging.error(f'IntegrityError: {e}')
            return web.json_response({'error': 'IntegrityError'}, status=INTERNAL_SERVER_ERROR)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)

        result = await conn.execute(
            sql.select([sql.func.max(images.c.image_id).label('image_id')])
        )
        new_id = await result.fetchone()
    return web.json_response({'message': f"Created with image_id: {str(dict(new_id)['image_id'])}"}, status=CREATED)


async def image_get(request, body) -> web.Response:
    dataset_id = body['dataset_id']
    try:
        async with request.app['db'].acquire() as conn:
            records = []
            async for record in conn.execute(
                    images.select().where(images.c.dataset_id == dataset_id).order_by(images.c.image_id)):
                record = dict(record)
                record['created_ts'] = dt_converter(record['created_ts'])
                record['updated_ts'] = dt_converter(record['updated_ts'])
                records.append(record)
            if not records:
                return web.json_response({'error': f'Images for that dataset with id: {dataset_id} not found'},
                                         status=NOT_FOUND)
            return web.json_response(data=records)
    except Exception as e:
        logging.error(f'Unexpected Error: {e}')
        return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)


async def image_update(request, body) -> web.Response:
    image_id = body['image_id']
    body['updated_ts'] = datetime.utcnow()
    async with request.app['db'].acquire() as conn:
        try:
            result = await conn.execute(images.update().where(images.c.image_id == image_id).values(body))
            if result.rowcount == 0:
                return web.json_response({'error': f'Image with id: {image_id} not found'}, status=NOT_FOUND)
        except IntegrityError as e:
            logging.error(f'IntegrityError: {e}')
            return web.json_response({'error': 'IntegrityError'}, status=INTERNAL_SERVER_ERROR)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)

        return web.json_response({'message': f'Image with id: {image_id} is updated'}, status=OK)


async def image_delete(request, body) -> web.Response:
    image_id = body['image_id']
    async with request.app['db'].acquire() as conn:
        try:
            result = await conn.execute(images.delete().where(images.c.image_id == image_id))
            if result.rowcount == 0:
                return web.json_response({'error': f'Image with id: {image_id} not found'}, status=NOT_FOUND)
            return web.json_response(status=204)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)


async def label_post(request, body) -> web.Response:
    if 'parameters' in body:
        try:
            body['parameters'] = json.loads(body['parameters'])
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return web.json_response({'error': "Can't convert parameters"})
    async with request.app['db'].acquire() as conn:
        try:
            await conn.execute(labels.insert().values(body))
        except IntegrityError as e:
            logging.error(f'IntegrityError: {e}')
            return web.json_response({'error': 'IntegrityError'}, status=INTERNAL_SERVER_ERROR)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)

        result = await conn.execute(
            sql.select([sql.func.max(labels.c.label_id).label('label_id')])
        )
        new_id = await result.fetchone()
    return web.json_response({'message': f"Created with label_id: {str(dict(new_id)['label_id'])}"}, status=CREATED)


async def label_get(request, body) -> web.Response:
    label_id = body['label_id']
    try:
        async with request.app['db'].acquire() as conn:
            cursor = await conn.execute(
                labels.select().where(labels.c.label_id == label_id).order_by(labels.c.label_id))
            record = await cursor.fetchone()
            if not record:
                return web.json_response({'error': f'Label with id: {label_id} not found'}, status=NOT_FOUND)
            record = dict(record)
            record['created_ts'] = dt_converter(record['created_ts'])
            record['updated_ts'] = dt_converter(record['updated_ts'])
            return web.json_response(data=record)
    except Exception as e:
        logging.error(f'Unexpected Error: {e}')
        return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)


async def label_update(request, body) -> web.Response:
    label_id = body['label_id']
    body['updated_ts'] = datetime.utcnow()
    async with request.app['db'].acquire() as conn:
        try:
            result = await conn.execute(labels.update().where(labels.c.label_id == label_id).values(body))
            if result.rowcount == 0:
                return web.json_response({'error': f'Label with id: {label_id} not found'}, status=NOT_FOUND)
        except IntegrityError as e:
            logging.error(f'IntegrityError: {e}')
            return web.json_response({'error': 'IntegrityError'}, status=INTERNAL_SERVER_ERROR)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)

        return web.json_response({'message': f'Label with id: {label_id} is updated'}, status=OK)


async def label_delete(request, body) -> web.Response:
    label_id = body['label_id']
    async with request.app['db'].acquire() as conn:
        try:
            result = await conn.execute(labels.delete().where(labels.c.label_id == label_id))
            if result.rowcount == 0:
                return web.json_response({'error': f'Label with id: {label_id} not found'}, status=NOT_FOUND)
            return web.json_response(status=204)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)


async def annotation_post(request, body) -> web.Response:
    async with request.app['db'].acquire() as conn:
        try:
            await conn.execute(annotations.insert().values(body))
            return web.json_response({'message': f"Created annotation image_id: {body['image_id']}"},
                                     status=CREATED)
        except IntegrityError as e:
            logging.error(f'IntegrityError: {e}')
            return web.json_response({'error': 'IntegrityError'}, status=INTERNAL_SERVER_ERROR)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)


async def annotation_get(request, body) -> web.Response:
    image_id = body['image_id']
    try:
        async with request.app['db'].acquire() as conn:
            cursor = await conn.execute(annotations.select().where(annotations.c.image_id == image_id))
            record = await cursor.fetchone()
            if not record:
                return web.json_response({'error': f'Annotation for image id: {image_id} not found'}, status=NOT_FOUND)
            record = dict(record)
            record['created_ts'] = dt_converter(record['created_ts'])
            record['updated_ts'] = dt_converter(record['updated_ts'])
            return web.json_response(data=record)
    except Exception as e:
        logging.error(f'Unexpected Error: {e}')
        return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)


async def annotation_update(request, body) -> web.Response:
    image_id = body['image_id']
    body['updated_ts'] = datetime.utcnow()
    async with request.app['db'].acquire() as conn:
        try:
            result = await conn.execute(annotations.update().where(annotations.c.image_id == image_id).values(body))
            if result.rowcount == 0:
                return web.json_response({'error': f'Annotation for image id: {image_id} not found'}, status=NOT_FOUND)
            return web.json_response({'message': f'Annotation for image id: {image_id} is updated'}, status=OK)
        except IntegrityError as e:
            logging.error(f'IntegrityError: {e}')
            return web.json_response({'error': 'IntegrityError'}, status=INTERNAL_SERVER_ERROR)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)


async def annotation_delete(request, body) -> web.Response:
    image_id = body['image_id']
    async with request.app['db'].acquire() as conn:
        try:
            result = await conn.execute(annotations.delete().where(annotations.c.image_id == image_id))
            if result.rowcount == 0:
                return web.json_response({'error': f'Annotation for image id: {image_id} not found'}, status=NOT_FOUND)
            return web.json_response(status=204)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')
            return web.json_response({'error': 'Server Error'}, status=INTERNAL_SERVER_ERROR)

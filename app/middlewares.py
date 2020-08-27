from aiohttp import web
import logging
from app.handlers import *
from app.statuscodes import BAD_REQUEST
from jsonschema import validate
from jsonschema.exceptions import ValidationError

JSON_HANDLERS = [project_post, project_update, project_delete,
                 dataset_post, dataset_get, dataset_update, dataset_delete,
                 image_post, image_get, image_update, image_delete,
                 annotation_post, annotation_get, annotation_update, annotation_delete,
                 label_post, label_get, label_update, label_delete]


@web.middleware
async def json_checker(request, handler):
    '''
    Middleware for checking requests content_type and validating requests body.

    In case when request has a JSON payload middleware must check everything with jsonschema.
    '''

    logging.info(f'New request for handler: {handler.__name__}')

    if handler in JSON_HANDLERS:
        if request.content_type != 'application/json':
            logging.error(f'Request without json payload: {await request.text()}')
            return web.json_response({'error': 'Request without json payload'}, status=BAD_REQUEST)
        body = await request.json()
        logging.info(f'Request body: {body}')
        try:
            validate(body, SCHEMA[handler.__name__])
            if 'annotations' in body:
                validate(body['annotations'], GEOJSON)
        except ValidationError as e:
            logging.error(f'ValidationError: {e}')
            return web.json_response({'error': 'Check JSON fields and types'}, status=BAD_REQUEST)
        return await handler(request, body)
    else:
        return await handler(request)

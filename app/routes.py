from app.handlers import *


def setup_routes(app):
    app.router.add_get('/echo', echo)
    app.router.add_get('/{name}', variable_handler)
    # Projects routes
    app.router.add_get('/api/v1/projects', project_get, name='project_get')
    app.router.add_post('/api/v1/projects', project_post, name='project_post')
    app.router.add_patch('/api/v1/projects', project_update, name='project_update')
    app.router.add_delete('/api/v1/projects', project_delete, name='project_delete')

    # Datasets routes
    app.router.add_get('/api/v1/datasets', dataset_get, name='dataset_get')
    app.router.add_post('/api/v1/datasets', dataset_post, name='dataset_post')
    app.router.add_patch('/api/v1/datasets', dataset_update, name='dataset_update')
    app.router.add_delete('/api/v1/datasets', dataset_delete, name='dataset_delete')

    # Images routes
    app.router.add_get('/api/v1/images', image_get, name='image_get')
    app.router.add_post('/api/v1/images', image_post, name='image_post')
    app.router.add_patch('/api/v1/images', image_update, name='image_update')
    app.router.add_delete('/api/v1/images', image_delete, name='image_delete')

    # Labels routes
    app.router.add_get('/api/v1/labels', label_get, name='label_get')
    app.router.add_post('/api/v1/labels', label_post, name='label_post')
    app.router.add_patch('/api/v1/labels', label_update, name='label_update')
    app.router.add_delete('/api/v1/labels', label_delete, name='label_delete')

    # Annotations routes
    app.router.add_get('/api/v1/annotations', annotation_get, name='annotation_get')
    app.router.add_post('/api/v1/annotations', annotation_post, name='annotation_post')
    app.router.add_patch('/api/v1/annotations', annotation_update, name='annotation_update')
    app.router.add_delete('/api/v1/annotations', annotation_delete, name='annotation_delete')

    # Andrew Slesarenko (swen295@gmail.com)

    # User routes

    app.router.add_post('/api/v1/session/login', session_login, name='session_login')
    app.router.add_post('/api/v1/session/logout', session_logout, name='session_logout')
    app.router.add_post('/api/v1/session/info', session_info, name='session_info')

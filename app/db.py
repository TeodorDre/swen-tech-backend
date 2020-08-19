from sqlalchemy import (
    MetaData, Table, Column, TIMESTAMP, BigInteger,
    TEXT, ForeignKeyConstraint, Integer, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

# TODO: timestamp -> timestampTZ
meta = MetaData()

users = Table(
    'users', meta,
    Column('client_id', Integer, primary_key=True, nullable=False),
    Column('client_name', TEXT, nullable=False, unique=False),
    Column('client_email', TEXT, nullable=False, unique=True),
    Column('password', TEXT, nullable=False, unique=False),

    Column('created_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    Column('updated_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    schema='markup'
)

sessions = Table(
    'sessions', meta,
    Column('client_id', Integer, unique=True, nullable=False),
    Column('session_id', TEXT, nullable=False, unique=True),
    Column('created_ts', TIMESTAMP, server_default=func.now(), nullable=False),

    ForeignKeyConstraint(['client_id'], [users.c.client_id],
                         name='sessions_client_id_fkey',
                         ondelete='CASCADE'),
    UniqueConstraint('client_id', 'session_id', name='cl_sess'),
    schema='markup'
)

projects = Table(
    'projects', meta,
    Column('project_id', Integer, primary_key=True, nullable=False),
    Column('project_name', TEXT, nullable=False, unique=True),
    Column('project_description', TEXT, nullable=True),
    Column('created_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    Column('updated_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    schema='markup'
)

datasets = Table(
    'datasets', meta,
    Column('dataset_id', Integer, primary_key=True, nullable=False),
    Column('dataset_name', TEXT, nullable=False),
    Column('dataset_description', TEXT, nullable=True),
    Column('project_id', Integer, nullable=False),
    Column('created_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    Column('updated_ts', TIMESTAMP, server_default=func.now(), nullable=False),

    # Indexes
    ForeignKeyConstraint(['project_id'], [projects.c.project_id],
                         name='datasets_project_id_fkey',
                         ondelete='CASCADE'),
    UniqueConstraint('dataset_name', 'project_id', name='ds_proj'),
    schema='markup'
)
images = Table(
    'images', meta,
    Column('image_id', Integer, primary_key=True, nullable=False),
    Column('image_name', TEXT, nullable=False),
    Column('image_description', TEXT, nullable=True),
    Column('image_link', TEXT, nullable=False),
    Column('width', Integer, nullable=False),
    Column('height', Integer, nullable=False),
    Column('dataset_id', Integer, nullable=False),
    Column('created_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    Column('updated_ts', TIMESTAMP, server_default=func.now(), nullable=False),

    # Indexes #
    ForeignKeyConstraint(['dataset_id'], [datasets.c.dataset_id],
                         name='images_dataset_id_fkey',
                         ondelete='CASCADE'),
    UniqueConstraint('image_name', 'dataset_id', name='im_ds'),
    UniqueConstraint('image_link', 'dataset_id', name='link_ds'),
    schema='markup'
)

annotations = Table(
    'annotations', meta,
    Column('image_id', BigInteger, nullable=False, unique=True),
    Column('annotations', JSONB, nullable=False),
    Column('created_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    Column('updated_ts', TIMESTAMP, server_default=func.now(), nullable=False),

    # Indexes #
    ForeignKeyConstraint(['image_id'], [images.c.image_id],
                         name='annotations_image_id_fkey',
                         ondelete='CASCADE'),
    schema='markup'
)

labels = Table(
    'labels', meta,
    Column('label_id', Integer, nullable=False, primary_key=True),
    Column('label_name', TEXT, nullable=False),
    Column('label_description', TEXT, nullable=True),
    Column('color', TEXT, nullable=False),
    Column('parameters', JSONB, nullable=True),
    Column('created_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    Column('updated_ts', TIMESTAMP, server_default=func.now(), nullable=False),
    schema='markup'

)


def create_tables(engine) -> None:
    '''
    Function for creating all needed for work tables
    in already created database.
    '''
    meta = MetaData()
    logging.info('Create all tables')
    meta.create_all(bind=engine, tables=[projects, datasets, images, annotations, labels, users])


def drop_tables(engine) -> None:
    '''
    Function for dropping tables
    '''
    meta = MetaData()
    logging.info('Drop all tables')
    meta.drop_all(bind=engine, tables=[projects, datasets, images, annotations, labels, users])


if __name__ == '__main__':
    from configuration import DB_CONFIG, DSN
    from sqlalchemy import create_engine
    import logging

    logging.basicConfig(
        level=logging.DEBUG,
        format='[{asctime}][{levelname}] - {name}: {message}', style='{')

    engine = create_engine(DSN.format(**DB_CONFIG))
    drop_tables(engine)
    create_tables(engine)

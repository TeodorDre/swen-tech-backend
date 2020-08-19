import sys
import logging
import psycopg2

from configuration import DB_CONFIG, DSN
from psycopg2.extras import execute_values
from mimesis.schema import Schema

from bootstrap.schemas import SCHEMAS


def insert_dummy(cur, schema: str, table: str, fields: str, template: str, data: list) -> None:
    """
    Function for bulk insertion of generated data

    :param cur: database cursor
    :param schema: db schema
    :param table: schema table
    :param fields: table fields
    :param template: insertion template
    :param data: list with all needed data
    """
    execute_values(cur=cur,
                   sql=f"INSERT INTO {schema}.{table} {fields} VALUES %s",
                   argslist=data,
                   template=template,
                   page_size=100)


def dummy_data(db_config: dict) -> None:
    """
    Insert dummy data into test database

    :param db_config:  database configuration
    """
    try:
        with psycopg2.connect(dsn=DSN.format(**db_config)) as connection:
            logging.info('Connected to PostgresDB')
            with connection.cursor() as cursor:
                for i in SCHEMAS:
                    logging.info(f"Insert dummy data into {i['table']}")
                    schema = Schema(schema=i['fields'])
                    while True:
                        try:
                            insert_dummy(cur=cursor,
                                         schema=i['schema'],
                                         table=i['table'],
                                         fields=i['values'],
                                         template=i['template'],
                                         data=schema.create(iterations=i['quantity']))
                            break
                        except psycopg2.IntegrityError as e:
                            logging.info(f'DataBase IntegrityError error: {e}')
                            # connection.rollback()
                            # break

                        connection.commit()

    except (Exception, psycopg2.OperationalError) as e:
        sys.exit(f'System error: {e}')
    logging.info('Task Complete')


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.DEBUG,
        format='[{asctime}][{levelname}] - {name}: {message}', style='{'
    )
    # Set configurations
    db_config = DB_CONFIG

    dummy_data(db_config=db_config)

import logging
import sys

from src.app import create_app


def setup_logging(config: dict):
    logging.basicConfig(
        level=config['logger_level'],
        format=config['format'],
        style=config['style'],
    )


def run_app(port: int):
    print(sys.path[0])
    create_app()


if __name__ == '__main__':
    run_app()

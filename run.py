import logging
import sys


def setup_logging(config: dict):
    logging.basicConfig(
        level=config['logger_level'],
        format=config['format'],
        style=config['style'],
    )


def run_app():
    print(sys.path[0])


if __name__ == '__main__':
    run_app()

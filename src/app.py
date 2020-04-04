from pathlib import Path
import os
from src.server.code.store import JSONStore


class ApplicationError:
    def __init__(self, name, message):
        self.name = name
        self.message = message

        print(name, message)


class BaseServer:
    def __init__(self):
        self.port = 3330
        self.store = None

    def init_services(self):
        current_file_folder = __file__

        store_path = Path(current_file_folder, '..', 'server', 'storage', 'store.json').resolve()

        try:
            open(store_path, 'r')
        except FileNotFoundError as error:
            if error.errno == 2:
                os.makedirs(Path(current_file_folder, '..', 'server', 'storage').resolve(), exist_ok=True)
                open(store_path, 'w')

        self.store = JSONStore(store_path)


server = BaseServer()

server.init_services()

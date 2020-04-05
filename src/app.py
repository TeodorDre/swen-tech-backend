from pathlib import Path
import os
from src.store import JSONStore



class Application:
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


def create_app():
    app = Application()

    app.init_services()

    return app

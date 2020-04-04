from src.app import ApplicationError
import json

STORE_ERROR_NAME = 'StoreError'


class StoreError(ApplicationError):
    def __init__(self, message, details):
        super().__init__(STORE_ERROR_NAME, message)

        self.details = details
        self.statusCode = 500


class JSONStore:
    def __init__(self, path):
        self.path = path

        self.cache = None

    def set_cache(self, data):
        self.cache = json.loads(data)

    def set(self, key, value):
        self.cache[key] = value

        try:
            serialized_data = json.dumps(self.cache)

            stream = open(self.path, encoding='utf-8', mode="w")
            stream.write(serialized_data)

            stream.close()
        except IOError as e:
            print(e)

    def get(self, key):
        return self.cache[key]

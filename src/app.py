class BaseServer:
    def __init__(self):
        self.port = 3330
        self.store = None

    def init_services(self):
        print('init Services')


server = BaseServer()

server.init_services()

import json


class Controller():
    __tornado = None
    _app = None

    def __init__(self, tornado, app, action):
        self.__tornado = tornado
        self._app = app
        func = getattr(self, action)
        func()

    def getArgument(self, name, default):
        return self.__tornado.get_argument(name, default=default)

    def json(self, data):
        data = json.dumps(data)
        self.__tornado.write(data)

    def display(self, name, title, items={}):
        self.__tornado.render(name, title=title, items=items)

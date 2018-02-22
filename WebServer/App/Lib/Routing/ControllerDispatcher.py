import tornado.web
import re
import importlib


class ControllerDispatcher(tornado.web.RequestHandler):
    __app = None

    def initialize(self, app):
        self.__app = app

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def dispatch(self, action):
        method = self.request.method.lower()
        router = self.__app.make('Router').list()
        routerList = router[method]
        for key in routerList:
            ret = re.search(key, action, re.I)
            if(ret is not None):
                param = routerList[key].split('@')
                module = importlib.import_module(param[0])
                obj = getattr(module, param[1])
                obj(self, self.__app, ret.group(1))
                break

    def get(self, action):
        self.dispatch(action)

    def post(self, action):
        self.dispatch(action)

    def put(self, action):
        self.dispatch(action)

    def delete(self, action):
        self.dispatch(action)

import re
import importlib
import tornado.web
import traceback


class ControllerDispatcher(tornado.web.RequestHandler):
    __app = None

    def initialize(self, app):
        self.__app = app

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def write_error(self, status_code, **kwargs):
        if(status_code == 404):
            self.write("404 Not Found")
        else:
            self.write("Gosh darnit, user! You caused a %d error." % status_code)

    def dispatch(self, action):
        try:
            method = self.request.method.lower()
            router = self.__app.make('Router').list()
            routerList = router[method]
            for key in routerList:
                ret = re.search(key, action, re.I)
                if(ret is not None):
                    param = routerList[key].split('@')
                    module = importlib.import_module(param[0])
                    if(hasattr(module, param[1]) is True):
                        obj = getattr(module, param[1])
                        if(hasattr(obj, ret.group(1)) is True):
                            return obj(self, self.__app, ret.group(1))
                            break
            self.set_status(404)
            self.write_error(404)
        except Exception as e:
            self.__app.make('Log').write(traceback.format_exc())
            items = {'error': traceback.format_exc()}
            self.set_status(500)
            self.write_error(500, items)

    def get(self, action):
        self.dispatch(action)

    def post(self, action):
        self.dispatch(action)

    def put(self, action):
        self.dispatch(action)

    def delete(self, action):
        self.dispatch(action)

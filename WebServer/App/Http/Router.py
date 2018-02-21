import tornado.web
import re
import importlib


router = {
    'socket': 'Http.Controllers.Socket@Socket',
    'getData/?(\w*)$': 'Http.Controllers.GetDataHandler@GetDataHandler',
}


class Router(tornado.web.RequestHandler):
    __app = None

    def initialize(self, app):
        self.__app = app

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self, action):
        for key in router:
            ret = re.search(key, action, re.I)
            if(ret is not None):
                param = router[key].split('@')
                module = importlib.import_module(param[0])
                obj = getattr(module, param[1])
                print(obj(ret.groups()))
                break
        self.write(action)

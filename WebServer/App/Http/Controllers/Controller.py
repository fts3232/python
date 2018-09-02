import json
from datetime import date, datetime

class Controller():
    __tornado = None
    _app = None

    def __init__(self, tornado, app, action):
        self.__tornado = tornado
        self._app = app
        func = getattr(self, action)
        func()

    def json_serial(self,obj):

        if isinstance(obj, (datetime, date)):
            serial = obj.isoformat()
            return serial
        raise TypeError ("Type %s not serializable" % type(obj))

    def getArgument(self, name, default=False):
        return self.__tornado.get_argument(name, default=default)

    def json(self, data):
        data = json.dumps(data,default=self.json_serial)
        self.__tornado.write(data)

    def display(self, name, title, items={}):
        self.__tornado.render(name, title=title, items=items)

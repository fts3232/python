import tornado.web
from Business.JavBus import JavBus


class SettingHandler(tornado.web.RequestHandler):
    __pool = None

    def initialize(self, pool):
        self.__pool = pool
        pass

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self, action):
        func = getattr(self, action)
        func()

    def createDB(self):
        JavBus(self.__pool).check_table()
        respon_json = tornado.escape.json_encode({'status': True, 'msg': "创建完成"})
        self.write(respon_json)

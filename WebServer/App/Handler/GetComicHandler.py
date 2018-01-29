import tornado.web
import sys
sys.path.append("../")
from Business.DM5 import DM5


class GetComicHandler(tornado.web.RequestHandler):

    def initialize(self):
        pass

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        ret = DM5().run()
        respon_json = tornado.escape.json_encode(ret)
        self.write(respon_json)

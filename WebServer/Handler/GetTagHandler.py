import tornado.web
import sys
sys.path.append("../")
from Model.Tag import Tag


class GetTagHandler(tornado.web.RequestHandler):
    __db = None
    __tag_model = None

    def initialize(self, pool):
        self.__db = pool.conn()
        self.__tag_model = Tag(self.__db)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        ret = self.__tag_model.getAll()
        self.__db.release()
        respon_json = tornado.escape.json_encode(ret)
        self.write(respon_json)

import tornado.web
import pickle


class GetLiveHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        fo = open('../host.pkl', 'rb+')
        ret = fo.read()
        live_list = pickle.loads(ret)
        respon_json = tornado.escape.json_encode(live_list)
        self.write(respon_json)

import tornado.web
import pickle
import os


class GetLiveHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        path = os.path.join(os.getcwd(), 'Storage/live.pkl')
        fo = open(path, 'rb+')
        ret = fo.read()
        live_list = pickle.loads(ret)
        for x in live_list:
            live_list[x] = sorted(live_list[x].items(), key=lambda item: item[1]['state'], reverse=True)
        respon_json = tornado.escape.json_encode(live_list)
        self.write(respon_json)

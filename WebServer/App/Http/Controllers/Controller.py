import tornado.web
import json


class Controller(tornado.web.RequestHandler):

    def initialize(self):
        pass

    def get(self, action):
        self.write('<html><body><p>1232</p></body></html>')

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def json(self, data):
        respon_json = tornado.escape.json_encode(data)
        self.write(respon_json)

    def display(self):
        self.write('<html><body><p>1232</p></body></html>')
        pass

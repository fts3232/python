from tornado.websocket import WebSocketHandler
import json
import importlib


class SocketHandler(WebSocketHandler):
    __pool = None
    users = set()  # 用来存放在线用户的容器

    def initialize(self, pool):
        self.__pool = pool

    def open(self):
        pass
        # self.users.add(self)  # 建立连接后添加用户到容器中
        # for u in self.users:  # 向已在线用户发送消息
        #     u.write_message(u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def sendMessage(self, event, message=''):
        self.write_message({'event': event, 'msg': message})

    def on_message(self, message):
        message = json.loads(message)
        event = message['event'][0].upper() + message['event'][1:]
        module = importlib.import_module('Business.SocketEvent.{method}'.format(method=event))
        obj = getattr(module, event)
        event = obj(options={'pool': self.__pool, 'print': self.sendMessage, 'data': event})
        event.run()

    def on_close(self):
        pass
        # self.users.remove(self)# 用户关闭连接后从容器中移除用户
        # for u in self.users:
        #     u.write_message(u"[%s]-[%s]-离开聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求

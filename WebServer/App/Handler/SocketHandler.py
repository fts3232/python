import os
from tornado.websocket import WebSocketHandler
import json
import re
import subprocess
import threading
import sys
sys.path.append("../")
from Helpers.functions import findMovie
from Business.JavBus import JavBus


class SocketHandler(WebSocketHandler):
    __pool = None

    def initialize(self, pool):
        self.__pool = pool

    users = set()  # 用来存放在线用户的容器

    def open(self):
        print(self)
        # self.users.add(self)  # 建立连接后添加用户到容器中
        # for u in self.users:  # 向已在线用户发送消息
        #     u.write_message(u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def on_message(self, message):
        message = json.loads(message)
        if(message['event'] == 'scan'):
            self.scan()
        elif(message['event'] == 'play'):
            self.play(message['msg'])
        elif(message['event'] == 'update-movie'):
            JavBus(self.__pool, self.scanPrint).updateMovie(message['msg']['movie_id'], message['msg']['identifier'])
        elif(message['event'] == 'spider'):
            self.spider()
        elif(message['event'] == 'open-dir'):
            self.openDir(message['msg'])
        # for u in self.users:  # 向在线用户广播消息
        #     u.write_message(u"[%s]-[%s]-说：%s" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))

    def on_close(self):
        pass
        # self.users.remove(self)# 用户关闭连接后从容器中移除用户
        # for u in self.users:
        #     u.write_message(u"[%s]-[%s]-离开聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def check_origin(self, origin):
        return True  # 允许WebSocket的跨域请求

    def scanPrint(self, msg):
        self.write_message({'event': 'scan', 'msg': msg})

    def spiderPrint(self, msg):
        self.write_message({'event': 'spider', 'msg': msg})

    def scan(self):
        roots = ['E:\迅雷下载', 'D:\QQDownload', 'D:\Downloads']
        identifiers = []
        for root in roots:
            for path in os.listdir(root):
                temp = "{root}/{path}".format(root=root, path=path)
                ret = os.path.splitext(temp)
                if((os.path.isfile(temp) and ret[1].lower() in ['.avi', '.mp4']) or os.path.isdir(temp)):
                    ret = re.findall('([A-Za-z]{2,})-?(\d{3,4})(-\d+)?', path)
                    if(len(ret) > 0):
                        ret = ret[-1]
                        num = ret[1]
                        if(len(num) >= 4 and num[0] == '0' and ret[0] != 'heyzo'):
                            num = num[1:]
                        if(ret[2] != ''):
                            identifier = "{series}-{num}-{extra}".format(series=ret[0], num=num, extra=ret[2][1:])
                        else:
                            identifier = "{series}-{num}".format(series=ret[0], num=num)
                        ret = re.findall('\d{6,}', path)
                        if(len(ret) > 0):
                            identifier = path
                        identifiers.append(identifier)
        task = threading.Thread(target=self.scanThreading, args=(identifiers,))
        task.start()

    def spider(self):
        task = threading.Thread(target=self.spiderThreading, args=())
        task.start()

    def scanThreading(self, identifiers):
        JavBus(self.__pool, self.scanPrint).search(identifiers)

    def spiderThreading(self):
        JavBus(self.__pool, self.spiderPrint).run()

    def play(self, identifier):
        try:
            msg = '播放成功'
            roots = ['E:\迅雷下载', 'D:\QQDownload', 'D:\Downloads']
            ret = findMovie(roots, identifier, ['.avi', '.mp4'])
            if(ret is None):
                raise Exception('文件不存在')
            ret = subprocess.Popen('"{path}"'.format(path=ret), shell=True)
        except Exception as e:
            msg = '播放失败'
            print(e)
        self.write_message({'event': 'play', 'msg': msg})

    def openDir(self, identifier):
        try:
            msg = '打开成功'
            roots = ['E:\迅雷下载', 'D:\QQDownload', 'D:\Downloads']
            ret = findMovie(roots, identifier, ['.avi', '.mp4'])
            if(ret is None):
                raise Exception('文件夹不存在')
            ret = subprocess.Popen('explorer "{path}"'.format(path=os.path.dirname(ret)), shell=True)
        except Exception as e:
            msg = '打开失败'
            print(e)
        self.write_message({'event': 'play', 'msg': msg})

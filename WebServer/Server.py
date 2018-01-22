import tornado.ioloop
import tornado.web
import sys
import os
import json
import re
import subprocess
import threading
sys.path.append("../")
from Mysql import ConnectionPool
from JavBus import JavBus
from tornado.websocket import WebSocketHandler
import difflib
import math


config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'db': 'JavBus',
    'charset': 'utf8',
    'max_connection': 20,
    'min_connection': 2,
}
pool = ConnectionPool(config)

# def find(roots, filename):
#     returnData = False
#     if(type(roots) == str):
#         for path in os.listdir(roots):
#             if(filename.lower() in path.lower() or filename.lower().replace('-', '') in path.lower()):
#                 temp = "{root}/{path}".format(root=roots, path=path)
#                 ret = os.path.splitext(temp)
#                 if(os.path.isfile(temp) and ret[1].lower() in ['.avi', '.mp4']):
#                     seq = difflib.SequenceMatcher(None, filename, path)
#                     ratio = seq.ratio() * 100
#                     if(returnData is False or returnData['ratio'] < ratio):
#                         returnData = {'root': roots, 'path': path, 'ratio': ratio}
#                 elif(os.path.isdir(temp)):
#                     returnData = findMovie(temp, filename)
#     else:
#         for root in roots:
#             for path in os.listdir(root):
#                 if(filename.lower() in path.lower() or filename.lower().replace('-', '') in path.lower()):
#                     temp = "{root}/{path}".format(root=root, path=path)
#                     ret = os.path.splitext(temp)
#                     if(os.path.isfile(temp) and ret[1].lower() in ['.avi', '.mp4']):
#                         seq = difflib.SequenceMatcher(None, filename, path)
#                         ratio = seq.ratio() * 100
#                         if(returnData is False or returnData['ratio'] < ratio):
#                             returnData = {'root': root, 'path': path, 'ratio': ratio}
#                     elif(os.path.isdir(temp)):
#                         returnData = findMovie(temp, filename)
#     return returnData


def findMovie(roots, filename, suffix=None):
    if(type(roots) == str):
        roots = [roots]
    ratio = 0
    data = None
    for root in roots:
        for path in os.listdir(root):
            if((filename.lower() in path.lower() or filename.lower().replace('-', '') in path.lower()) or filename.lower() in root.lower()):
                temp = os.path.join(root, path)
                if(os.path.isfile(temp) and os.path.splitext(temp)[1].lower() in suffix):
                    path_ratio = math.ceil(difflib.SequenceMatcher(None, path, filename).quick_ratio() * 100)
                    if(path_ratio > ratio):
                        ratio = path_ratio
                        data = temp
                elif(os.path.isdir(temp)):
                    return findMovie(temp, filename, suffix)
    return data


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class GetTagHandler(tornado.web.RequestHandler):
    def get(self):
        db = pool.conn()
        ret = db.select('select TAG_ID,TAG_NAME from TAG ORDER BY TAG_NAME')
        db.release()
        respon_json = tornado.escape.json_encode(ret)
        self.write(respon_json)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


class GetDataHandler(tornado.web.RequestHandler):
    def get(self):
        p = int(self.get_argument('p'))
        size = int(self.get_argument('size'))
        title = str(self.get_argument('title', default=''))
        star = str(self.get_argument('star', default=''))
        tag = str(self.get_argument('tag', default=''))
        db = pool.conn()
        offset = (p - 1) * size
        if(title != ''):
            ret = db.select('select MOVIE_ID,TITLE,IDENTIFIER,TAG,STAR,PUBLISH_TIME from MOVIE WHERE IDENTIFIER LIKE :SEARCH OR TITLE LIKE :SEARCH ORDER BY UPDATED_TIME DESC,PUBLISH_TIME DESC,CREATED_TIME DESC LIMIT {offset},{size}'.format(offset=offset, size=size), {'SEARCH': '%{search}%'.format(search=title)})
        elif(star != ''):
            ret = db.select('select MOVIE_ID,TITLE,IDENTIFIER,TAG,STAR,PUBLISH_TIME from MOVIE WHERE FIND_IN_SET(:STAR,STAR) ORDER BY UPDATED_TIME DESC,PUBLISH_TIME DESC,CREATED_TIME DESC LIMIT {offset},{size}'.format(offset=offset, size=size), {'STAR': star})
        elif(tag != ''):
            ret = db.select('select MOVIE_ID,TITLE,IDENTIFIER,TAG,STAR,PUBLISH_TIME from MOVIE WHERE FIND_IN_SET(:TAG,TAG) ORDER BY UPDATED_TIME DESC,PUBLISH_TIME DESC,CREATED_TIME DESC LIMIT {offset},{size}'.format(offset=offset, size=size), {'TAG': tag})
        else:
            ret = db.select('select MOVIE_ID,TITLE,IDENTIFIER,TAG,STAR,PUBLISH_TIME from MOVIE ORDER BY UPDATED_TIME DESC,PUBLISH_TIME DESC,CREATED_TIME DESC LIMIT {offset},{size}'.format(offset=offset, size=size))
        for x in ret:
            x['PUBLISH_TIME'] = x['PUBLISH_TIME'].strftime('%Y-%m-%d')
            path = '../JavBus/Movie/{identifier}'.format(identifier=x['IDENTIFIER'])
            sample = []
            x['LINK'] = []
            x['IMAGE'] = 'http://localhost:8000/static/now_printing.jpg'
            x['PLAY'] = True if(findMovie(['E:\迅雷下载', 'D:\QQDownload', 'D:\Downloads'], x['IDENTIFIER'], ['.avi', '.mp4']) is not None) else False
            links = db.select('select LINK,PUBLISH_TIME from DOWNLOAD_LINK where MOVIE_ID = :MOVIE_ID', {'MOVIE_ID': x['MOVIE_ID']})
            for link in links:
                link['PUBLISH_TIME'] = str(link['PUBLISH_TIME'])
                x['LINK'].append(link)
            if(x['TAG'] != '' and x['TAG'] is not None):
                tags = db.select('select TAG_ID,TAG_NAME from TAG where TAG_ID IN({tag})'.format(tag=x['TAG']))
                x['TAG'] = tags
            if(x['STAR'] != '' and x['STAR'] is not None):
                stars = db.select('select STAR_ID,STAR_NAME from STAR where STAR_ID IN({star})'.format(star=x['STAR']))
                for index, star in enumerate(stars):
                    stars[index]['IMAGE'] = 'http://localhost:8000/static/Star/{name}.jpg'.format(name=star['STAR_NAME'])
                x['STAR'] = stars
            if(os.path.isdir(path)):
                for file in os.listdir(path):
                    if(file != 'cover.jpg'):
                        sample.append("http://localhost:8000/static/Movie/{dir}/{file}".format(file=file, dir=x['IDENTIFIER']))
                x['IMAGE'] = 'http://localhost:8000/static/Movie/{identifier}/cover.jpg'.format(identifier=x['IDENTIFIER'])
            samples = db.select('select URL from SAMPLE where MOVIE_ID = :MOVIE_ID', {'MOVIE_ID': x['MOVIE_ID']})
            x["SAMPLE"] = samples
        db.release()
        respon_json = tornado.escape.json_encode(ret)
        self.write(respon_json)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')


class SocketHandler(WebSocketHandler):

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
            JavBus(pool, self.scanPrint).updateMovie(message['msg']['movie_id'], message['msg']['identifier'])
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
        JavBus(pool, self.scanPrint).search(identifiers)

    def spiderThreading(self):
        JavBus(pool, self.spiderPrint).run()

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


settings = {
    'template_path': 'Build',
    'static_path': '../JavBus',
    'static_url_prefix': '/static/',
    'debug': True
}

application = tornado.web.Application([
    (r"/", IndexHandler),
    (r"/getData", GetDataHandler),
    (r"/getTag", GetTagHandler),
    (r"/socket", SocketHandler),
    (r"/css/(.*)", tornado.web.StaticFileHandler, dict(path='Build/css')),
    (r"/js/(.*)", tornado.web.StaticFileHandler, dict(path='Build/js')),
], **settings)


application.listen(8000)
tornado.ioloop.IOLoop.instance().start()

import os
import tornado.web
import sys
sys.path.append("../")
from Helpers.functions import findMovie
from Model.Movie import Movie
from Model.Tag import Tag
from Model.Star import Star
from Model.DownloadLink import DownloadLink
from Model.Sample import Sample
import re


class GetDataHandler(tornado.web.RequestHandler):
    __db = None

    def initialize(self, pool):
        self.__db = pool.conn()
        self.__movie_model = Movie(self.__db)
        self.__tag_model = Tag(self.__db)
        self.__star_model = Star(self.__db)
        self.__downloadlink_model = DownloadLink(self.__db)
        self.__sample_model = Sample(self.__db)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        p = int(self.get_argument('p', default=1))
        size = int(self.get_argument('size', default=12))
        title = self.get_argument('title', default=None)
        star = self.get_argument('star', default=None)
        tag = self.get_argument('tag', default=None)
        canPlay = True if self.get_argument('canPlay', default=0) == '1' else False
        offset = (p - 1) * size
        options = {'size': size, 'title': title, 'star': star, 'tag': tag, 'offset': offset}
        if(canPlay is True):
            identifiers = self.getCanPlay()
            if(options['title'] is None and options['star'] is None and options['tag'] is None):
                identifiers = identifiers[offset:offset + size]
            options['identifiers'] = identifiers
        ret = self.getData(options)
        self.__db.release()
        respon_json = tornado.escape.json_encode(ret)
        self.write(respon_json)

    def getCanPlay(self):
        roots = ['E:\迅雷下载', 'D:\QQDownload', 'D:\Downloads']
        identifiers = []
        for root in roots:
            paths = os.listdir(root)
            paths = sorted(paths, key=lambda x: os.path.getmtime(os.path.join(root, x)), reverse=True)
            for path in paths:
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
                        identifiers.append("'{}'".format(identifier))
        return identifiers

    def getData(self, options):
        ret = self.__movie_model.get(options)
        for x in ret:
            # 可否播放
            storage_path = os.path.join(os.getcwd(), 'Storage/JavBus/Movie')
            path = os.path.join(storage_path, x['IDENTIFIER'])
            x['PLAY'] = True if(findMovie(['E:\迅雷下载', 'D:\QQDownload', 'D:\Downloads'], x['IDENTIFIER'], ['.avi', '.mp4']) is not None) else False
            # 发布时间
            x['PUBLISH_TIME'] = x['PUBLISH_TIME'].strftime('%Y-%m-%d')
            # 下载链接
            links = self.__downloadlink_model.get(x['MOVIE_ID'])
            x['LINK'] = []
            for link in links:
                link['PUBLISH_TIME'] = str(link['PUBLISH_TIME'])
                x['LINK'].append(link)
            # 封面图
            x['IMAGE'] = 'http://localhost:8000/static/now_printing.jpg'
            if(os.path.isfile(os.path.join(path, 'cover.jpg'))):
                x['IMAGE'] = 'http://localhost:8000/static/Movie/{identifier}/cover.jpg'.format(identifier=x['IDENTIFIER'])
            # 分类
            if(x['TAG'] != '' and x['TAG'] is not None):
                tags = self.__tag_model.get(x['TAG'])
                x['TAG'] = tags
            # 演员
            if(x['STAR'] != '' and x['STAR'] is not None):
                stars = self.__star_model.get(x['STAR'])
                for index, star in enumerate(stars):
                    stars[index]['IMAGE'] = 'http://localhost:8000/static/Star/{name}.jpg'.format(name=star['STAR_NAME'])
                x['STAR'] = stars
            # 样本图链接
            samples = self.__sample_model.get(x['MOVIE_ID'])
            x["SAMPLE"] = samples
        return ret

import os
import re
from Helpers.functions import findMovie
from Model.Movie import Movie
from Model.Tag import Tag
from Model.Star import Star
from Model.DownloadLink import DownloadLink
from Model.Sample import Sample


class Av():
    _app = None

    def __init__(self, app):
        self._app = app
        pass

    def getData(self, options):
        db = self._app.make('ConnectionPool').conn()
        movie_model = Movie(db)
        star_model = Star(db)
        tag_model = Tag(db)
        downloadlink_model = DownloadLink(db)
        sample_model = Sample(db)
        ret = movie_model.get(options)
        for x in ret:
            # 可否播放
            storage_path = os.path.join(os.getcwd(), 'Storage/JavBus/Movie')
            path = os.path.join(storage_path, x['IDENTIFIER'])
            x['PLAY'] = True if(findMovie(['E:\迅雷下载', 'D:\QQDownload', 'D:\Downloads'], x['IDENTIFIER'], ['.avi', '.mp4']) is not None) else False
            # 发布时间
            x['PUBLISH_TIME'] = x['PUBLISH_TIME'].strftime('%Y-%m-%d')
            # 下载链接
            links = downloadlink_model.get(x['MOVIE_ID'])
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
                tags = tag_model.get(x['TAG'])
                x['TAG'] = tags
            # 演员
            if(x['STAR'] != '' and x['STAR'] is not None):
                stars = star_model.get(x['STAR'])
                for index, star in enumerate(stars):
                    stars[index]['IMAGE'] = 'http://localhost:8000/static/Star/{name}.jpg'.format(name=star['STAR_NAME'])
                x['STAR'] = stars
            # 样本图链接
            samples = sample_model.get(x['MOVIE_ID'])
            x["SAMPLE"] = samples
        db.release()
        return ret

    def getCanPlay(self):
        roots = ['E:\迅雷下载', 'D:\QQDownload', 'D:\Downloads']
        identifiers = []
        for root in roots:
            if(os.path.exists(root)):
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

    def getTag(self):
        db = self._app.make('ConnectionPool').conn()
        tag_model = Tag(db)
        tag = tag_model.getAll()
        db.release()
        return tag

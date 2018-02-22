from time import time
from Config.DM5 import config
from Lib.Visitor import Visitor


class Comic():
    'DM5'
    __visitor = None

    def __init__(self):
        self.__visitor = Visitor()

    def get_news(self):
        ret = self.__visitor.send_request("{host}{get_news_path}{timestamp}".format(host=config['host'], get_news_path=config['get_news_path'], timestamp=int(time()) - 300), {'host': 'www.dm5.com'}).visit()
        ret = ret.replace('null', 'None')
        ret = ret.replace('true', 'True')
        ret = ret.replace('false', 'False')
        data = eval(ret)
        comic_list = []
        for x in data['UpdateComicItems']:
            comic_list.append({'url': "{host}/{path}".format(host=config['host'], path=x['LastPartUrl']), 'title': x['Title'], 'episodes': x['ShowLastPartName'], 'cover': x['ShowPicUrlB']})
            # print("标题：{title} 集数：{partname} 封面：{cover}".format(title=x['Title'], partname=x['ShowLastPartName'], cover=x['ShowConver']))
        return comic_list

    def run(self):
        ret = self.get_news()
        return ret

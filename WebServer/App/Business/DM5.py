import sys
from time import time
sys.path.append("../")
from Lib.Visitor import Visitor


class DM5(Visitor):
    'DM5'
    __host = 'http://www.dm5.com/manhua-new/dm5.ashx?action=getupdatecomics&d='
    __visitor = None

    def __init__(self):
        self.__visitor = Visitor()

    def get_news(self):
        ret = self.__visitor.send_request("{host}{timestamp}".format(host=self.__host, timestamp=int(time()) - 300)).visit()
        ret = ret.replace('null', 'None')
        data = eval(ret)
        comic_list = []
        for x in data['UpdateComicItems']:
            comic_list.append({'id': x['ID'], 'title': x['Title'], 'episodes': x['ShowLastPartName'], 'cover': x['ShowConver']})
            # print("标题：{title} 集数：{partname} 封面：{cover}".format(title=x['Title'], partname=x['ShowLastPartName'], cover=x['ShowConver']))
        return comic_list

    def run(self):
        ret = self.get_news()
        print(ret)

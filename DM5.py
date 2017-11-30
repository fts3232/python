from bs4 import BeautifulSoup
from Visitor import Visitor
import threading
import time
import os
import re
import execjs


class DM5(Visitor):
    'DM5'
    __host = 'http://cnc.dm5.com'
    __get_news_path = '/manhua-new'
    __visitor = None

    def __init__(self, visitor):
        self.__visitor = visitor

    def get_news(self):
        ret = self.__visitor.send_request("{host}{path}".format(host=self.__host, path=self.__get_news_path)).visit()
        soup = BeautifulSoup(ret, "html.parser")
        tags = soup.find_all('div', {'class': 'innr3'})
        comic_list = []
        for tag in tags:
            ret = tag.find_all('li', {'class': 'red_lj'})
            pattern = re.compile(r'<img src="(.*?)".*<a href="(.*?)" title="(.*?)" target="_blank">')
            match = pattern.findall(ret)
            comic_list.append({'pic': match[0], 'link': "{host}/{path}".format(host=self.__host, path=match[1]), 'title': match[2]})
        return comic_list

    def run(self):
        ret = self.get_news()
        print(ret)
        # ret = self.__visitor.send_request('http://cnc.dm5.com/m557761/').visit()
        # soup = BeautifulSoup(ret, "html.parser")
        # page_count = re.search('var DM5_IMAGE_COUNT=(\d+?);', ret).group(1)
        # cid = re.search('var DM5_CID=(\d+?);', ret).group(1)
        # page = 1
        # mkey = soup.find('input', {"id": 'dm5_key'})['value']
        # pic_list = []
        # while page <= int(page_count):
        #     url = 'http://cnc.dm5.com/m557761/chapterfun.ashx?cid={cid}&page={page}&key={key}&language={language}&gtk={gtk}'.format(cid=cid, page=page, key=mkey, language=1, gtk=6)
        #     ret = self.__visitor.send_request(url, options={'referer': 'http://cnc.dm5.com/m557761/'}).visit()
        #     ret = execjs.eval(ret)
        #     pic_list += list(ret)
        #     page += 2
        #     time.sleep(1)
        #     pass
        # print(pic_list)


DM5(Visitor()).run()

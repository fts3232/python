from bs4 import BeautifulSoup
from Visitor import Visitor
import threading
import time
import os
import re


class DM5(Visitor):
    'DM5'
    __url = 'http://cnc.dm5.com/manhua-new'
    __visitor = None

    def __init__(self, visitor):
        self.__visitor = visitor

    def get_dir(self, name):
        today = time.strftime("%Y-%m-%d", time.localtime())
        parent_dir = "./JavBus/{today}".format(today=today)
        if(os.path.exists(parent_dir) is False):
            os.mkdir(parent_dir)
        child_dir = "{parent}/{child}".format(parent=parent_dir, child=name)
        if(os.path.exists(child_dir) is False):
            os.mkdir(child_dir)
        return child_dir

    def run(self):
        ret = self.__visitor.send_request('http://cnc.dm5.com/m557761/').visit()
        soup = BeautifulSoup(ret, "html.parser")
        page_count = re.search('var DM5_IMAGE_COUNT=(\d+?);', ret).group(1)
        cid = re.search('var DM5_CID=(\d+?);', ret).group(1)
        page = 1
        mkey = soup.find('input', {"id": 'dm5_key'})['value']
        url = 'http://cnc.dm5.com/m557761/chapterfun.ashx?cid={cid}&page={page}&key={key}&language={language}&gtk={gtk}'.format(cid=cid, page=page, key=mkey, language=1, gtk=6)
        ret = self.__visitor.send_request(url, options={'referer':'http://cnc.dm5.com/m557761/'}).visit()
        print(ret)
        # ret = self.__visitor.send_request(self.__url).visit()
        # soup = BeautifulSoup(ret, "html.parser")
        # tags = soup.find_all('li', {"class": 'red_lj'})
        # for tag in tags:
        #     title = tag.find('a').find('strong').text
        #     episodes = tag.find_all('a')[2].text
        #     url = tag.find_all('a')[2]['href']
        #     covers = tag.find('img')['src']
        #     date = re.search('\d+年\d+月\d+日', tag.text).group(0)
        #     print(date)
        #     print(covers)
        #     print(title,num)
        #     print(url)


DM5(Visitor()).run()

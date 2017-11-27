from bs4 import BeautifulSoup
from Visitor import Visitor
import threading
import time
import os
import re
import execjs


class DM5(Visitor):
    'DM5'
    __url = 'http://cnc.dm5.com/manhua-new'
    __visitor = None

    def __init__(self, visitor):
        self.__visitor = visitor

    def run(self):
        ret = self.__visitor.send_request('http://cnc.dm5.com/m557761/').visit()
        soup = BeautifulSoup(ret, "html.parser")
        page_count = re.search('var DM5_IMAGE_COUNT=(\d+?);', ret).group(1)
        cid = re.search('var DM5_CID=(\d+?);', ret).group(1)
        page = 1
        mkey = soup.find('input', {"id": 'dm5_key'})['value']
        pic_list = []
        while page <= int(page_count):
            url = 'http://cnc.dm5.com/m557761/chapterfun.ashx?cid={cid}&page={page}&key={key}&language={language}&gtk={gtk}'.format(cid=cid, page=page, key=mkey, language=1, gtk=6)
            ret = self.__visitor.send_request(url, options={'referer': 'http://cnc.dm5.com/m557761/'}).visit()
            ret = execjs.eval(ret)
            pic_list += list(ret)
            page += 2
            time.sleep(1)
            pass
        print(pic_list)


DM5(Visitor()).run()

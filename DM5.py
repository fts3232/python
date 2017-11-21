from bs4 import BeautifulSoup
from Visitor import Visitor
import threading
import time
import os
import re


class DM5(Visitor):
    'DM5'
    __url = 'http://cnc.dm5.com/manhua-new'

    def __init__(self):
        Visitor.__init__(self)

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
        ret = self.visit(self.__publish_page)
        urls = self.get_urls(ret)
        self.get_fast_url(urls)
        ret = self.visit(self.__url['url'])
        movie_list = self.get_movie_list(ret)
        threads = []
        for movie in movie_list:
            task = threading.Thread(target=self.visit_single, args=(movie,))
            threads.append(task)
            task.start()
            task.join()
            time.sleep(1)


DM5().run()

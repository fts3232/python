from bs4 import BeautifulSoup
from Visitor import Visitor
import threading
import time
import os
import re


class JavBus():
    'JavBus'
    # 发布页url
    __publish_page = 'https://announce.javbus2.pw/website.php'
    # 获取magnet的请求路径
    __get_magnet_path = '/ajax/uncledatoolsbyajax.php'
    # 访问的url
    __url = None
    # vistor类
    __visitor = None

    def __init__(self, visitor):
        self.__visitor = visitor

    # 获取发布页上的所有url
    def get_urls(self, body):
        soup = BeautifulSoup(body, "html.parser")
        tags = soup.find_all('a')
        urls = []
        for tag in tags:
            urls.append(tag['href'])
        return urls

    # 通过ping来获取速度最快的url
    def get_fast_url(self, urls):
        threads = []
        for url in urls:
            task = threading.Thread(target=self.ping, args=(url,))
            threads.append(task)
            task.start()
        for thread in threads:
            thread.join()
        print(self.__url)

    # 重写ping
    def ping(self, url):
        ret = self.__visitor.ping(self, url)
        if(ret['alive'] is True and (self.__url is None or ret['time'] <= self.__url['time'])):
            self.__url = ret

    # 获取列表
    def get_movie_list(self, body):
        soup = BeautifulSoup(body, "html.parser")
        tags = soup.find_all('a', class_="movie-box")
        movie_list = []
        for tag in tags:
            movie_list.append(tag['href'])
        print(movie_list)
        return movie_list

    # download sample图片
    def download_sample(self, url, path, filename):
        ret = self.__visitor.send_request(url).download(path, filename)
        return ret

    # 获取目录
    def get_dir(self, name):
        today = time.strftime("%Y-%m-%d", time.localtime())
        parent_dir = "./JavBus/{today}".format(today=today)
        if(os.path.exists(parent_dir) is False):
            os.mkdir(parent_dir)
        child_dir = "{parent}/{child}".format(parent=parent_dir, child=name)
        if(os.path.exists(child_dir) is False):
            os.mkdir(child_dir)
        return child_dir

    # 访问详情页
    def visit_single(self, url):
        body = self.visit(url)
        soup = BeautifulSoup(body, "html.parser")
        big_image = soup.find('a', {"class": "bigImage"}).find('img')
        title = big_image['title']
        big_image = big_image['src']
        print(big_image)
        print(title)
        identifier = soup.find('div', {"class": ["col-md-3", "info"]}).find_all('p')[0].find_all('span')[1]
        identifier = identifier.text
        print(identifier)
        dir_path = self.get_dir(identifier)
        ret = self.__visitor.send_request(big_image, options={"referer": url}).visit()
        fo = open("{path}/{filename}.jpg".format(path=dir_path, filename=identifier), "wb+")
        fo.write(ret)
        fo.close()
        self.get_magnet_link(body, url, dir_path)
        sample_box = soup.find_all('a', {"class": "sample-box"})
        if(len(sample_box) > 0):
            threads = []
            for i, sample in enumerate(sample_box):
                url = sample.find('img')['src']
                task = threading.Thread(target=self.download_sample, args=(url, dir_path, "sample-{i}.jpg".format(i=i)))
                threads.append(task)
                task.start()
                task.join()
                time.sleep(1)

    # 获取magnet链接
    def get_magnet_link(self, body, referer, dir_path):
        url = 'https://www.javbus.info' + self.__get_magnet_path
        gid = re.search('var gid = (.*?);', body).group(1)
        img = re.search("var img = '(.*?)';", body).group(1)
        url = url + "?gid={gid}&img={img}&uc=0&lang=zh".format(gid=gid, img=img)
        ret = self.__visitor.send_request(url, {"referer": referer}).visit()
        soup = BeautifulSoup(ret, "html.parser")
        tags = soup.find_all('tr')
        if(len(tags) > 0):
            fo = open("{parent}/magnet.txt".format(parent=dir_path), "a+")
            for tag in tags:
                href = tag.find_all('td')[0].find('a')['href']
                time = tag.find_all('td')[2].find('a').text.strip()
                fo.write("{href} {time}\n".format(href=href, time=time))
            fo.close()

    def run(self):
        ret = self.__visitor.send_request(self.__publish_page).visit()
        urls = self.get_urls(ret)
        self.get_fast_url(urls)
        ret = self.__visitor.send_request(self.__url['url']).visit()
        movie_list = self.get_movie_list(ret)
        threads = []
        for movie in movie_list:
            task = threading.Thread(target=self.visit_single, args=(movie,))
            threads.append(task)
            task.start()
            task.join()
            time.sleep(1)


JavBus(Visitor()).run()

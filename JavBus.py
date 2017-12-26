from bs4 import BeautifulSoup
from Visitor import Visitor
import threading
import time
import os
import re
import pickle
from Mysql import Mysql


class JavBus():
    'JavBus'
    # 发布页url
    __publish_page = 'https://announce.javbus2.pw/website.php'
    # 获取magnet的请求路径
    __get_magnet_path = '/ajax/uncledatoolsbyajax.php'
    # 访问的域名
    __host = None
    # vistor类
    __visitor = None
    # db类
    __db = None

    def __init__(self, visitor, db):
        self.__visitor = visitor
        self.__db = db
        self.checkTable()

    # 创建数据表
    def checkTable(self):
        try:
            sql = "SHOW TABLES LIKE 'MOVIE'"
            ret = self.__db.select(sql)
            if(len(ret) == 0):
                sql = "CREATE TABLE MOVIE(\
                       `MOVIE_ID` INT NOT NULL AUTO_INCREMENT,\
                       `IDENTIFIER` VARCHAR(30) NOT NULL,\
                       `TITLE`  VARCHAR(255) NOT NULL,\
                       `SAMPLE` TINYINT(1) NOT NULL DEFAULT 0,\
                       `MAGNET` TINYINT(1) NOT NULL DEFAULT 0,\
                       `CREATED_TIME` DATETIME DEFAULT CURRENT_TIMESTAMP,\
                       PRIMARY KEY (`MOVIE_ID`)\
                       )\
                       ENGINE=InnoDB\
                       DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci;"
                ret = self.__db.query(sql)
            sql = "SHOW TABLES LIKE 'LOG'"
            ret = self.__db.select(sql)
            if(len(ret) == 0):
                sql = "CREATE TABLE LOG(\
                       `LOG_ID` INT NOT NULL AUTO_INCREMENT,\
                       `CATEGORY` VARCHAR(30) NOT NULL,\
                       `DESCRIPTION`  TEXT NOT NULL,\
                       `CREATED_TIME` DATETIME DEFAULT CURRENT_TIMESTAMP,\
                       PRIMARY KEY (`LOG_ID`)\
                       )\
                       ENGINE=InnoDB\
                       DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci;"
                ret = self.__db.query(sql)
        except Exception as e:
            print('检查数据库失败')
            print(repr(e))

    # 获取域名
    def get_host(self):
        if(os.path.exists('./JavBus/host.pkl') is True):
            fo = open('./JavBus/host.pkl', 'rb+')
            ret = fo.read()
            self.__host = pickle.loads(ret)
            print('读取之前的host记录: ' + self.__host)
        else:
            body = self.__visitor.send_request(self.__publish_page).visit()
            soup = BeautifulSoup(body, "html.parser")
            tags = soup.find_all('a')
            urls_list = []
            for tag in tags:
                urls_list.append(tag['href'])
            print(urls_list)
            self.__host = self.__visitor.ping_list(urls_list)
            fo = open('./JavBus/host.pkl', 'wb+')
            fo.write(pickle.dumps(self.__host))
            fo.close()
        return self.__host

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
        body = self.__visitor.send_request(url).visit()
        soup = BeautifulSoup(body, "html.parser")
        # 番号
        identifier = soup.find('div', {"class": ["col-md-3", "info"]}).find_all('p')[0].find_all('span')[1]
        identifier = identifier.text
        # 生成文件夹
        dir_path = self.get_dir(identifier)
        # 封面图
        big_image = soup.find('a', {"class": "bigImage"}).find('img')
        # self.__visitor.send_request(big_image['src'], options={"referer": url}).download(dir_path, "{filename}.jpg".format(filename=identifier))
        # 标题
        title = big_image['title']
        # 是否存在sample图片
        sample_box = soup.find_all('a', {"class": "sample-box"})
        hasSample = 1 if len(sample_box) > 0 else 0
        # magnet
        hasMagnet = 1 if self.get_magnet_link(body, url, dir_path) is True else 0
        print("番号：{identifier} 片名：{title} 封面图片：{big_image}".format(identifier=identifier, title=title, big_image=big_image['src']))
        # 插入数据
        self.__db.begin()
        row = self.__db.find('SELECT MOVIE_ID,SAMPLE,MAGNET FROM MOVIE WHERE TITLE LIKE :TITLE AND IDENTIFIER = :IDENTIFIER', {'TITLE': title, 'IDENTIFIER': identifier})
        if(row is None):
            self.__db.insert('INSERT INTO MOVIE(IDENTIFIER,TITLE,SAMPLE,MAGNET) VALUES(:IDENTIFIER,:TITLE,:SAMPLE,:MAGNET)', {'TITLE': title, 'IDENTIFIER': identifier, 'SAMPLE': hasSample, 'MAGNET': hasMagnet})
        else:
            if(hasSample and row['SAMPLE'] == 0):
                self.__db.update('UPDATE MOVIE SET SAMPLE = 1 WHERE MOVIE_ID = :ID', {'ID': row['MOVIE_ID']})
            if(hasMagnet and row['MAGNET'] == 0):
                self.__db.update('UPDATE MOVIE SET MAGNET = 1 WHERE MOVIE_ID = :ID', {'ID': row['MOVIE_ID']})
        self.__db.commit()
        # 下载sample图片
        # if(hasSample):
        #     hasSample
        #     threads = []
        #     for i, sample in enumerate(sample_box):
        #         url = sample.find('img')['src']
        #         task = threading.Thread(target=self.download_sample, args=(url, dir_path, "sample-{i}.jpg".format(i=i)))
        #         threads.append(task)
        #         task.start()
        #         task.join()
        #         time.sleep(1)

    # 获取magnet链接
    def get_magnet_link(self, body, referer, dir_path):
        url = self.__host + self.__get_magnet_path
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
        return len(tags) > 0

    def startThreads(self, threads, num=1, sleep=1):
        arr = []
        for index, thread in enumerate(threads):
            index = index + 1
            arr.append(thread)
            if(index % num == 0 or len(threads) == index):
                for task in arr:
                    task.start()
                for task in arr:
                    task.join()
                arr = []
                time.sleep(sleep)

    def run(self):
        if(os.path.exists('./JavBus') is False):
            os.mkdir('./JavBus')
        self.get_host()
        ret = self.__visitor.send_request(self.__host).visit()
        movie_list = self.get_movie_list(ret)
        threads = []
        for index, movie in enumerate(movie_list[:5]):
            task = threading.Thread(target=self.visit_single, args=(movie,))
            threads.append(task)
        self.startThreads(threads=threads, num=2, sleep=1)


JavBus(Visitor(), Mysql()).run()

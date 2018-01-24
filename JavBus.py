from bs4 import BeautifulSoup
import threading
import time
import os
import re
import pickle
from Visitor import Visitor
from datetime import datetime


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
    # 连接池
    __pool = None
    # 需要爬的页数
    __page = 2

    __stdout = None

    __path = None

    def __init__(self, ConnectionPool, stdout=print):
        self.__visitor = Visitor(stdout)
        self.__pool = ConnectionPool
        self.__stdout = stdout
        self.check_table()
        self.__path = os.path.dirname(__file__) + '/JavBus'
        if(os.path.exists(self.__path) is False):
            os.mkdir(self.__path)
        self.get_host()

    # 创建数据表
    def check_table(self):
        try:
            conn = self.__pool.conn()
            sql = "SHOW TABLES LIKE 'MOVIE'"
            ret = conn.select(sql)
            if(len(ret) == 0):
                sql = "CREATE TABLE MOVIE(\
                       `MOVIE_ID` INT NOT NULL AUTO_INCREMENT,\
                       `CATEGORY` TINYINT(1) NOT NULL DEFAULT 1,\
                       `IDENTIFIER` VARCHAR(30) NOT NULL,\
                       `TITLE`  VARCHAR(255) NOT NULL,\
                       `STAR`  VARCHAR(255) DEFAULT NULL,\
                       `TAG`  VARCHAR(255) DEFAULT NULL,\
                       `PUBLISH_TIME` DATETIME NOT NULL,\
                       `CREATED_TIME` DATETIME DEFAULT CURRENT_TIMESTAMP,\
                       `UPDATED_TIME` DATETIME DEFAULT NULL,\
                       PRIMARY KEY (`MOVIE_ID`)\
                       )\
                       ENGINE=InnoDB\
                       DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci;"
                ret = conn.query(sql)
            sql = "SHOW TABLES LIKE 'LOG'"
            ret = conn.select(sql)
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
                ret = conn.query(sql)
            sql = "SHOW TABLES LIKE 'DOWNLOAD_LINK'"
            ret = conn.select(sql)
            if(len(ret) == 0):
                sql = "CREATE TABLE DOWNLOAD_LINK(\
                       `LINK_ID` INT NOT NULL AUTO_INCREMENT,\
                       `MOVIE_ID` VARCHAR(30) NOT NULL,\
                       `LINK`  TEXT NOT NULL,\
                       `PUBLISH_TIME` DATE NOT NULL,\
                       `CREATED_TIME` DATETIME DEFAULT CURRENT_TIMESTAMP,\
                       PRIMARY KEY (`LINK_ID`)\
                       )\
                       ENGINE=InnoDB\
                       DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci;"
                ret = conn.query(sql)
            sql = "SHOW TABLES LIKE 'TAG'"
            ret = conn.select(sql)
            if(len(ret) == 0):
                sql = "CREATE TABLE TAG(\
                       `TAG_ID` INT NOT NULL AUTO_INCREMENT,\
                       `TAG_NAME` VARCHAR(30) NOT NULL,\
                       `CREATED_TIME` DATETIME DEFAULT CURRENT_TIMESTAMP,\
                       PRIMARY KEY (`TAG_ID`)\
                       )\
                       ENGINE=InnoDB\
                       DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci;"
                ret = conn.query(sql)
            sql = "SHOW TABLES LIKE 'STAR'"
            ret = conn.select(sql)
            if(len(ret) == 0):
                sql = "CREATE TABLE STAR(\
                       `STAR_ID` INT NOT NULL AUTO_INCREMENT,\
                       `STAR_NAME`  TEXT NOT NULL,\
                       `CREATED_TIME` DATETIME DEFAULT CURRENT_TIMESTAMP,\
                       PRIMARY KEY (`STAR_ID`)\
                       )\
                       ENGINE=InnoDB\
                       DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci;"
                ret = conn.query(sql)
            sql = "SHOW TABLES LIKE 'SAMPLE'"
            ret = conn.select(sql)
            if(len(ret) == 0):
                sql = "CREATE TABLE SAMPLE(\
                       `SAMPLE_ID` INT NOT NULL AUTO_INCREMENT,\
                       `MOVIE_ID`  INT NOT NULL,\
                       `URL`  VARCHAR(255) NOT NULL,\
                       `CREATED_TIME` DATETIME DEFAULT CURRENT_TIMESTAMP,\
                       PRIMARY KEY (`SAMPLE_ID`)\
                       )\
                       ENGINE=InnoDB\
                       DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci;"
                ret = conn.query(sql)
            conn.release()
        except Exception as e:
            self.__stdout('检查数据库失败')
            self.__stdout(repr(e))

    # 获取域名
    def get_host(self):
        try:
            if(os.path.exists(self.__path + '/host.pkl') is not True):
                raise Exception('文件不存在')
            fo = open(self.__path + '/host.pkl', 'rb+')
            ret = fo.read()
            self.__host = pickle.loads(ret)
            self.__stdout('读取之前的host记录: ' + self.__host)
            ret = self.__visitor.ping(self.__host)
            if(ret['alive'] is not True):
                raise Exception('旧有记录ping不通')
        except Exception as e:
            body = self.__visitor.send_request(self.__publish_page).visit()
            soup = BeautifulSoup(body, "html.parser")
            tags = soup.find_all('a')
            urls_list = []
            for tag in tags:
                urls_list.append(tag['href'])
            self.__stdout(urls_list)
            self.__host = self.__visitor.ping_list(urls_list)
            fo = open(self.__path + '/host.pkl', 'wb+')
            fo.write(pickle.dumps(self.__host))
            fo.close()
            self.__stdout('host: ' + self.__host)
        return self.__host

    # 获取列表
    def get_movie_list(self, body):
        soup = BeautifulSoup(body, "html.parser")
        tags = soup.find_all('a', class_="movie-box")
        movie_list = []
        for tag in tags:
            movie_list.append(tag['href'])
        # self.__stdout(str(movie_list))
        return movie_list

    # 获取目录
    def get_dir(self, name):
        # today = time.strftime("%Y-%m-%d", time.localtime())
        parent_dir = self.__path
        if(os.path.exists(parent_dir) is False):
            os.mkdir(parent_dir)
        child_dir = "{parent}/{child}".format(parent=parent_dir, child=name)
        if(os.path.exists(child_dir) is False):
            os.makedirs(child_dir)
        return child_dir

    # 访问详情页
    def visit_single(self, url, movie_id=None):
        body = self.__visitor.send_request(url).visit()
        conn = self.__pool.conn()
        conn.begin()
        if(body is not None):
            soup = BeautifulSoup(body, "html.parser")
            # 番号
            identifier = soup.find('div', {"class": ["col-md-3", "info"]}).find_all('p')[0].find_all('span')[1]
            identifier = identifier.text
            # 生成文件夹
            dir_path = self.get_dir('Movie/' + identifier)
            # 封面图
            cover = soup.find('a', {"class": "bigImage"}).find('img')['src']
            if(os.path.exists(os.path.join(dir_path, "cover.jpg")) is False):
                self.__visitor.send_request(cover, options={"referer": url}).download(dir_path, "cover.jpg")
            # 标题
            title = soup.find('h3').text
            title = title.replace(identifier + ' ', '')
            # 是否存在sample图片
            sample_box = soup.find_all('a', {"class": "sample-box"})
            has_sample = 1 if len(sample_box) > 0 else 0
            self.__stdout("番号：{identifier} 片名：{title} 封面图片：{cover}".format(identifier=identifier, title=title, cover=cover))
            # 插入数据
            movie_row = conn.find('SELECT MOVIE_ID FROM MOVIE WHERE TITLE LIKE :TITLE AND IDENTIFIER = :IDENTIFIER', {'TITLE': title, 'IDENTIFIER': identifier})
            if(movie_id is not None or movie_row is None):
                # 分类标签
                tags = soup.find('div', {"class": ["col-md-3", "info"]}).find_all('p')
                tag = []
                star = []
                if(tags is not None):
                    # tag
                    node_index = 0
                    for index, node in enumerate(tags):
                        if(node.text == '類別:'):
                            node_index = index + 1
                            continue
                        if(node_index == index):
                            tag_tags = node.find_all('span', {"class": "genre"})
                            for tag_tag in tag_tags:
                                row = conn.find('SELECT TAG_ID FROM TAG WHERE TAG_NAME = :TAG_NAME', {'TAG_NAME': tag_tag.find('a').text})
                                if(row is None):
                                    tag_id = conn.insert('INSERT INTO TAG(TAG_NAME) VALUES(:TAG_NAME)', {'TAG_NAME': tag_tag.find('a').text})
                                else:
                                    tag_id = row['TAG_ID']
                                tag.append(str(tag_id))
                # star
                star_tags = soup.find_all('a', {"class": ["avatar-box"]})
                star_dir = self.get_dir('Star')
                for star_tag in star_tags:
                    star_pic = star_tag.find('img')['src']
                    star_name = star_tag.find('span').text
                    if(os.path.exists(os.path.join(star_dir, '{name}.jpg'.format(name=star_name))) is False):
                        self.__visitor.send_request(star_pic).download(star_dir, '{name}.jpg'.format(name=star_name))
                    row = conn.find('SELECT STAR_ID FROM STAR WHERE STAR_NAME = :STAR_NAME', {'STAR_NAME': star_name})
                    if(row is None):
                        star_id = conn.insert('INSERT INTO STAR(STAR_NAME) VALUES(:STAR_NAME)', {'STAR_NAME': star_name})
                    else:
                        star_id = row['STAR_ID']
                    star.append(str(star_id))

                publish_time = tags[1].get_text()
                publish_time = publish_time.replace('發行日期: ', '')
                publish_time = publish_time if(publish_time != '0000-00-00') else str(datetime.now().strftime("%Y-%m-%d"))
                tag = ','.join(tag) if(tag != []) else None
                star = ','.join(star) if(star != []) else None
                if(movie_id is None):
                    movie_id = conn.insert('INSERT INTO MOVIE(IDENTIFIER,TITLE,TAG,STAR,PUBLISH_TIME,UPDATED_TIME) VALUES(:IDENTIFIER,:TITLE,:TAG,:STAR, :PUBLISH_TIME, NOW())', {'TITLE': title, 'IDENTIFIER': identifier, 'STAR': star, 'TAG': tag, 'PUBLISH_TIME': publish_time})
                else:
                    conn.update('UPDATE MOVIE SET IDENTIFIER = :IDENTIFIER, TITLE = :TITLE, TAG = :TAG, STAR = :STAR, PUBLISH_TIME = :PUBLISH_TIME WHERE MOVIE_ID = :MOVIE_ID', {'TITLE': title, 'IDENTIFIER': identifier, 'STAR': star, 'TAG': tag, 'PUBLISH_TIME': publish_time, 'MOVIE_ID': movie_id})
            else:
                movie_id = movie_row['MOVIE_ID']
            # # 获取magnet链接
            self.get_magnet_link(conn, movie_id, body, url, dir_path)
            # 下载sample图片
            if(movie_row is None or has_sample):
                for i, sample in enumerate(sample_box):
                    count = conn.count('SELECT COUNT(SAMPLE_ID) FROM SAMPLE WHERE URL = :URL', {'URL': sample['href']})
                    if(count == 0):
                        conn.insert('INSERT INTO SAMPLE(MOVIE_ID,URL) VALUES(:MOVIE_ID,:URL)', {'MOVIE_ID': movie_id, 'URL': sample['href']})
        else:
            identifier = url.replace(self.__host + '/', '')
            row = conn.insert('INSERT INTO MOVIE(IDENTIFIER,TITLE,PUBLISH_TIME,UPDATED_TIME) VALUES(:IDENTIFIER,:TITLE,NOW(), NOW())', {'TITLE': identifier, 'IDENTIFIER': identifier})
        conn.commit()
        conn.release()

    # 获取magnet链接
    def get_magnet_link(self, conn, movie_id, body, referer, dir_path):
        url = self.__host + self.__get_magnet_path
        gid = re.search('var gid = (.*?);', body).group(1)
        img = re.search("var img = '(.*?)';", body).group(1)
        url = url + "?gid={gid}&img={img}&uc=0&lang=zh".format(gid=gid, img=img)
        ret = self.__visitor.send_request(url, options={"referer": referer}).visit()
        if(ret is not None):
            soup = BeautifulSoup(ret, "html.parser")
            tags = soup.find_all('tr')
            if(len(tags) > 0):
                for tag in tags:
                    if(tag.find_all('td')[0].find('a') is not None):
                        link = tag.find_all('td')[0].find('a')['href']
                        time = tag.find_all('td')[2].find('a').text.strip()
                        row = conn.count('SELECT COUNT(*) AS TOTAL FROM DOWNLOAD_LINK WHERE MOVIE_ID = :MOVIE_ID AND LINK = :LINK', {'MOVIE_ID': movie_id, 'LINK': link})
                        if(row == 0):
                            conn.insert('INSERT INTO DOWNLOAD_LINK(MOVIE_ID,LINK,PUBLISH_TIME) VALUES(:MOVIE_ID,:LINK,:PUBLISH_TIME)', {'MOVIE_ID': movie_id, 'LINK': link, 'PUBLISH_TIME': time})

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

    def search(self, identifiers):
        self.__stdout('开始爬取数据...')
        conn = self.__pool.conn()
        threads = []
        for identifier in identifiers:
            count = conn.count('SELECT COUNT(*) FROM MOVIE WHERE IDENTIFIER = :IDENTIFIER', {'IDENTIFIER': identifier})
            if(count == 0):
                task = threading.Thread(target=self.visit_single, args=("{host}/{identifier}".format(host=self.__host, identifier=identifier),))
                threads.append(task)
        self.startThreads(threads=threads, num=2, sleep=2.5)
        conn.release()
        self.__stdout('结束...')

    def updateMovie(self, movie_id, identifier):
        self.__stdout('开始爬取数据...')
        self.visit_single("{host}/{identifier}".format(host=self.__host, identifier=identifier), movie_id)
        self.__stdout('结束...')

    def run(self):
        self.__stdout('开始爬取数据...')
        page = 0
        while(page < self.__page):
            page += 1
            ret = self.__visitor.send_request(self.__host + '/page/' + str(page)).visit()
            if(ret is not None):
                movie_list = self.get_movie_list(ret)
                temp = movie_list.copy()
                for index, movie in enumerate(temp):
                    temp[index] = "'" + movie.replace(self.__host + '/', '') + "'"
                temp = ','.join(temp)
                conn = self.__pool.conn()
                count = conn.count('SELECT COUNT(*) FROM MOVIE WHERE IDENTIFIER IN(' + temp + ')')
                if(count == 30):
                    continue
                threads = []
                for index, movie in enumerate(movie_list):
                    task = threading.Thread(target=self.visit_single, args=(movie,))
                    threads.append(task)
                self.startThreads(threads=threads, num=2, sleep=2)
        #self.__pool.close()
        self.__stdout('结束...')

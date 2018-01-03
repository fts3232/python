from bs4 import BeautifulSoup
import threading
import time
import os
import re
import pickle


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

    def __init__(self, visitor, ConnectionPool, stdout=print):
        self.__visitor = visitor
        self.__pool = ConnectionPool
        self.__stdout = stdout

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
                       `TAG` TEXT NOT NULL,\
                       `SAMPLE` TINYINT(1) NOT NULL DEFAULT 1,\
                       `CREATED_TIME` DATETIME DEFAULT CURRENT_TIMESTAMP,\
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
            conn.release()
        except Exception as e:
            self.__stdout('检查数据库失败')
            self.__stdout(repr(e))

    # 获取域名
    def get_host(self):
        try:
            if(os.path.exists('./JavBus/host.pkl') is not True):
                raise Exception('文件不存在')
            fo = open('./JavBus/host.pkl', 'rb+')
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
            fo = open('./JavBus/host.pkl', 'wb+')
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
        self.__stdout(movie_list)
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
        conn = self.__pool.conn()
        if(body is not None):
            soup = BeautifulSoup(body, "html.parser")
            # 番号
            identifier = soup.find('div', {"class": ["col-md-3", "info"]}).find_all('p')[0].find_all('span')[1]
            identifier = identifier.text
            # 生成文件夹
            dir_path = self.get_dir(identifier)
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
            conn.begin()
            row = conn.find('SELECT MOVIE_ID,SAMPLE FROM MOVIE WHERE TITLE LIKE :TITLE AND IDENTIFIER = :IDENTIFIER', {'TITLE': title, 'IDENTIFIER': identifier})
            if(row is None):
                # 分类标签
                tags = soup.find('div', {"class": ["col-md-3", "info"]}).find_all('p')
                category_tag_index = None
                category = []
                for index, tag in enumerate(tags):
                    if(tag.has_attr('class') and 'header' in tag['class']):
                        category_tag_index = index + 1
                        continue
                    if(index == category_tag_index):
                        category_tags = tag.find_all('span', {"class": "genre"})
                        for category_tag in category_tags:
                            category.append(category_tag.find('a').text)
                        break
                category = ','.join(category)
                movie_id = conn.insert('INSERT INTO MOVIE(IDENTIFIER,TITLE,TAG,SAMPLE) VALUES(:IDENTIFIER,:TITLE,:TAG,:SAMPLE)', {'TITLE': title, 'IDENTIFIER': identifier, 'SAMPLE': has_sample, 'TAG': category})
            else:
                movie_id = row['MOVIE_ID']
                if(has_sample and row['SAMPLE'] == 0):
                    conn.update('UPDATE MOVIE SET SAMPLE = 1 WHERE MOVIE_ID = :ID', {'ID': row['MOVIE_ID']})
            # 获取magnet链接
            self.get_magnet_link(conn, movie_id, body, url, dir_path)
            conn.commit()
            conn.release()
            # 下载sample图片
            if(row is None or (has_sample and row['SAMPLE'] == 0)):
                threads = []
                for i, sample in enumerate(sample_box):
                    url = sample.find('img')['src']
                    task = threading.Thread(target=self.download_sample, args=(url, dir_path, "sample-{i}.jpg".format(i=i)))
                    threads.append(task)
                self.startThreads(threads, num=2, sleep=2)

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

    def run(self):
        self.check_table()
        if(os.path.exists('./JavBus') is False):
            os.mkdir('./JavBus')
        self.get_host()
        page = 0
        while(page < self.__page):
            page += 1
            ret = self.__visitor.send_request(self.__host + '/page/' + str(page)).visit()
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
            for index, movie in enumerate(movie_list[:5]):
                task = threading.Thread(target=self.visit_single, args=(movie,))
                threads.append(task)
            self.startThreads(threads=threads, num=2, sleep=2)
        self.__pool.close()

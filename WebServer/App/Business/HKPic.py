from bs4 import BeautifulSoup
import time
import os
import re
import pickle
from Config.HKPic import config
from Lib.Visitor import Visitor


class HKPic(Visitor):
    'HKPic'
    # vistor类
    __visitor = None
    # 访问的域名
    __host = None
    # 连接池
    __pool = None

    __stdout = None

    __path = os.path.join(os.getcwd(), '../../Storage/HKPic')

    def __init__(self, ConnectionPool=None, stdout=print):
        self.__pool = ConnectionPool
        self.__visitor = Visitor()
        self.__stdout = stdout
        if(os.path.exists(self.__path) is False):
            os.mkdir(self.__path)

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
            body = self.__visitor.send_request(config['publish_page']).visit()
            pattern = re.compile(r'(.*)<br><br>')
            matches = pattern.findall(body)
            urls_list = []
            flag = False
            for match in matches:
                if(match == '最新IP'):
                    flag = True
                    continue
                elif(match == '比思備用域名'):
                    break
                if(flag is True):
                    urls_list.append(match)
            print(urls_list)
            self.__host = self.__visitor.ping_list(urls_list)
            fo = open(self.__path + '/host.pkl', 'wb+')
            fo.write(pickle.dumps(self.__host))
            fo.close()
            self.__stdout('host: ' + self.__host)
        return self.__host

    # 登录
    def login(self):
        url = "{host}{login_path}".format(host=self.__host, login_path=config['login_path'])
        ret = self.__visitor.send_request(url, data={'username': config['username'], 'password': config['password']}).visit()
        return ret

    # 获取目录
    def get_dir(self, name):
        today = time.strftime("%Y-%m-%d", time.localtime())
        parent_dir = "./HKPic/{today}".format(today=today)
        if(os.path.exists(parent_dir) is False):
            os.mkdir(parent_dir)
        child_dir = "{parent}/{child}".format(parent=parent_dir, child=name)
        if(os.path.exists(child_dir) is False):
            os.mkdir(child_dir)
        return child_dir

    def run(self):
        self.get_host()
        ret = self.login()
        print(ret)
        # body = self.__visitor.send_request(self.__host + config['forum_path']).visit()
        # print(body)
        pass
        # if(os.path.exists('./HKPic') is False):
        #     os.mkdir('./HKPic')
        # self.get_host()
        # self.login()
        # body = self.__visitor.send_request(self.__host + self.__forum_path).visit()
        # soup = BeautifulSoup(body, "html.parser")
        # tags = soup.find_all('a', {'class': 'xst'})
        # today = time.strftime("%m.%d", time.localtime())
        # for tag in tags:
        #     if(re.search(today, tag.text)):
        #         print(tag.text)
        #         body = self.__visitor.send_request("{host}/{path}".format(host=self.__host, path=tag['href'])).visit()
        #         pattern = re.compile(r'^(?!使用大陸)+([^<>\n\r]+?)<br />(?:\n\n[^<>\n\r]+?<br />)?(?:\n\n[^<>\n\r]+?<br />)?[\s\S]*?([\s\S]*?)<a href="(.*?)"', re.M)
        #         matches = pattern.findall(body)
        #         for match in matches:
        #             title = re.sub(r'([\?\\\/\|:\<\>\t\r\n ]+)|(\.\.\.$)', '', match[0])
        #             link = match[2]
        #             dir_path = self.get_dir(title)
        #             soup = BeautifulSoup(match[1], "html.parser")
        #             tags = soup.find_all('img')
        #             if(tags is not None):
        #                 for index, tag in enumerate(tags):
        #                     self.__visitor.send_request("{host}/{path}".format(host=self.__host, path=tag['file'])).download(dir_path, 'sample-{index}.jpg'.format(index=index))
        #                     time.sleep(1)
        #             fo = open("{path}/pan.txt".format(path=dir_path), "w+")
        #             fo.write(link)
        #             fo.close()
        #         break


HKPic().run()

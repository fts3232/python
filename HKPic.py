from bs4 import BeautifulSoup
from Visitor import Visitor
import time
import os
import re
import pickle
from Mysql import Mysql


class HKPic(Visitor):
    'HKPic'
    # 发布页
    __publish_url = 'http://caregirl.net/hkpic.html'
    # 登录地址
    __login_path = '/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes'
    # vistor类
    __visitor = None
    # 登录账户
    __username = 'fts3232'
    # 登录密码
    __password = '323232'
    # 板块地址
    __forum_path = '/forum.php?mod=forumdisplay&action=list&fid=215&filter=typeid&typeid=1042'
    # 访问的域名
    __host = None
    # db类
    __db = None

    def __init__(self, visitor, db):
        self.__visitor = visitor
        self.__db = db

    # 获取域名
    def get_host(self):
        if(os.path.exists('./HKPic/host.pkl') is True):
            fo = open('./HKPic/host.pkl', 'rb+')
            ret = fo.read()
            self.__host = pickle.loads(ret)
            print('读取之前的host记录: ' + self.__host)
        else:
            body = self.__visitor.send_request(self.__publish_url).visit()
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
            fo = open('./HKPic/host.pkl', 'wb+')
            fo.write(pickle.dumps(self.__host))
            fo.close()
        return self.__host

    # 登录
    def login(self):
        url = self.__host + self.__login_path
        ret = self.__visitor.send_request(url, data={'username': self.__username, 'password': self.__password}).visit()
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
        if(os.path.exists('./HKPic') is False):
            os.mkdir('./HKPic')
        self.get_host()
        self.login()
        body = self.__visitor.send_request(self.__host + self.__forum_path).visit()
        soup = BeautifulSoup(body, "html.parser")
        tags = soup.find_all('a', {'class': 'xst'})
        today = time.strftime("%m.%d", time.localtime())
        for tag in tags:
            if(re.search(today, tag.text)):
                print(tag.text)
                body = self.__visitor.send_request("{host}/{path}".format(host=self.__host, path=tag['href'])).visit()
                pattern = re.compile(r'^(?!使用大陸)+([^<>\n\r]+?)<br />(?:\n\n[^<>\n\r]+?<br />)?(?:\n\n[^<>\n\r]+?<br />)?[\s\S]*?([\s\S]*?)<a href="(.*?)"', re.M)
                matches = pattern.findall(body)
                for match in matches:
                    title = re.sub(r'([\?\\\/\|:\<\>\t\r\n ]+)|(\.\.\.$)', '', match[0])
                    link = match[2]
                    dir_path = self.get_dir(title)
                    soup = BeautifulSoup(match[1], "html.parser")
                    tags = soup.find_all('img')
                    if(tags is not None):
                        for index, tag in enumerate(tags):
                            self.__visitor.send_request("{host}/{path}".format(host=self.__host, path=tag['file'])).download(dir_path, 'sample-{index}.jpg'.format(index=index))
                            time.sleep(1)
                    fo = open("{path}/pan.txt".format(path=dir_path), "w+")
                    fo.write(link)
                    fo.close()
                break


HKPic(Visitor(), Mysql()).run()

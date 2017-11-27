from bs4 import BeautifulSoup
from Visitor import Visitor
import time
import os
import re


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
    __host = None

    def __init__(self, visitor):
        self.__visitor = visitor

    def get_host(self):
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
        return self.__host

    def login(self):
        url = self.__host + self.__login_path
        ret = self.__visitor.send_request(url, data={'username': self.__username, 'password': self.__password}).visit()
        return ret

    def run(self):
        self.get_host()
        self.login()
        body = self.__visitor.send_request(self.__host + self.__forum_path).visit()
        soup = BeautifulSoup(body, "html.parser")
        tags = soup.find_all('a', {'class': 'xst'})
        today = time.strftime("%m.%d", time.localtime())
        link_list = []
        for tag in tags:
            if(re.search(today,tag.text)):
                link_list.append(tag)
                print(tag.text)


HKPic(Visitor()).run()
import random
import urllib
import subprocess
import urllib.request
import socket
import time


class Visitor:
    '访问类'
    __visits = 1
    __max_visits = 2

    def __init__(self):
        pass

    def create_ip(self):
        return "{0}.{1}.{2}.{3}".format(random.randint(1, 254), random.randint(1, 254), random.randint(1, 254), random.randint(1, 254))

    def get_host(self, url):
        host = urllib.parse.urlparse(url).netloc
        if(host == ''):
            host = url
        return host

    def get_headers(self, options={}):
        headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'X-Forwarded-For': self.create_ip(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': '*',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1'
        }
        if('host' in options):
            headers['host'] = options['host']
        if('referer' in options):
            headers['referer'] = options['referer']
        return headers

    def visit(self, url, options={}, data=None, decode=True):
        try:
            socket.setdefaulttimeout(10)
            request = urllib.request.Request(url, data=data, headers=self.get_headers(options))
            response = urllib.request.urlopen(request)
            ret = response.read()
            if(decode is True):
                ret = ret.decode('utf-8', 'ignore')
            response.close()
            if(ret is None):
                raise Exception("None")
            print("访问 {url} 成功，访问次数：{num}".format(url=url, num=self.__visits))
            self.__visits = 1
            return ret
        except Exception as e:
            print("访问 {url} 失败，错误：{error}，访问次数：{num}".format(url=url, num=self.__visits, error=e.message))
            time.sleep(2)
            self.__visits += 1
            if(self.__visits <= self.__max_visits):
                self.visit(url, options)

    def ping(self, url):
        try:
            host = self.get_host(url)
            ret = subprocess.Popen(["ping.exe", host],
                                   shell=True,
                                   stdout=subprocess.PIPE)
            ret = str(ret.stdout.read())
            alive = True
            ms = ret[ret.rindex('=') + 2:ret.rindex('ms')]
        except Exception as e:
            alive = False
            ms = 'unkown'
        print("ping {host} 完成，平均时间为{time}".format(host=host, time=ms))
        return {'url': url, 'time': int(ms), 'alive': alive}

import random
import urllib
import subprocess
import urllib.request
import socket
import time


class Visitor:
    '访问类'
    __total_request_num = 1
    __max_request_num = 2
    __result = None
    __url = None

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

    def send_request(self, url, data=None, options={}):
        try:
            self.__url = url
            socket.setdefaulttimeout(10)
            request = urllib.request.Request(url, data=data, headers=self.get_headers(options))
            response = urllib.request.urlopen(request)
            self.__result = response.read()
            response.close()
            print("发送请求 {url} 成功，发送次数：{num}".format(url=url, num=self.__visits))
            self.__total_request_num = 1
        except Exception as e:
            print("发送 {url} 失败，错误：{error}，发送次数：{num}".format(url=url, num=self.__visits, error=e.message))
            time.sleep(2)
            self.__total_request_num += 1
            if(self.__total_request_num <= self.__max_request_num):
                self.send_request(url, options=options, data=data)
        return self

    def download(self, path, filename):
        if(self.__result is None):
            print('{url} 下载失败'.format(url=self.__url))
        else:
            fo = open("{path}/{filename}".format(path=path, filename=filename), "wb+")
            fo.write(self.__result)
            fo.close()
            print('{url} 下载成功'.format(url=self.__url))

    def visit(self):
        ret = None
        if(self.__result is None):
            print('{url} 访问失败'.format(url=self.__url))
        else:
            ret = self.__result.decode('utf-8', 'ignore')
            print('{url} 访问成功'.format(url=self.__url))
        return ret

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

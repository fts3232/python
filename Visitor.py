import random
import urllib
import subprocess
import socket
import time
import http.cookiejar
import threading


class VisitResult:
    '结果类'
    # 访问的结果
    __result = None
    # 访问的url
    __url = None

    def __init__(self, url, result):
        self.__result = result
        self.__url = url

    # 下载
    def download(self, path, filename):
        if(self.__result is None):
            print('{url} 下载失败'.format(url=self.__url))
        else:
            fo = open("{path}/{filename}".format(path=path, filename=filename), "wb+")
            fo.write(self.__result)
            fo.close()
            print('{url} 下载成功'.format(url=self.__url))

    # 访问
    def visit(self):
        ret = None
        if(self.__result is None):
            print('{url} 访问失败'.format(url=self.__url))
        else:
            ret = self.__result.decode('utf-8', 'ignore')
            print('{url} 访问成功'.format(url=self.__url))
        return ret

    def get_result(self):
        return self.__result


class Visitor:
    '访问类'
    # 当前请求次数
    __total_request_num = 1
    # 最大请求次数
    __max_request_num = 2
    # opener
    __urlOpener = None

    def __init__(self):
        # 使用cookie
        cookiejar = http.cookiejar.CookieJar()
        self.__urlOpener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))

    # 生成ip
    def create_ip(self):
        return "{0}.{1}.{2}.{3}".format(random.randint(1, 254), random.randint(1, 254), random.randint(1, 254), random.randint(1, 254))

    # 获取域名
    def get_host(self, url):
        host = urllib.parse.urlparse(url).netloc
        if(host == ''):
            host = url
        return host

    # 获取头部
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
        headers.update(options)
        return headers

    # 发送请求
    def send_request(self, url, data=None, options={}):
        try:
            result = None
            socket.setdefaulttimeout(10)
            if(data is not None):
                data = bytes(urllib.parse.urlencode(data), encoding='utf8')
            request = urllib.request.Request(url, data=data, headers=self.get_headers(options))
            response = self.__urlOpener.open(request)
            result = response.read()
            response.close()
            print("发送请求 {url} 成功，发送次数：{num}".format(url=url, num=self.__total_request_num))
            self.__total_request_num = 1
        except Exception as e:
            print("发送请求 {url} 失败，错误：{error}，发送次数：{num}".format(url=url, num=self.__total_request_num, error=str(e)))
            repr(e)
            if(e.code != '404'):
                time.sleep(2)
                self.__total_request_num += 1
                if(self.__total_request_num <= self.__max_request_num):
                    self.send_request(url, options=options, data=data)
            else:
                self.__total_request_num = 1
        return VisitResult(url, result)

    # ping
    def ping(self, url):
        try:
            host = self.get_host(url)
            ret = subprocess.Popen(["ping.exe", host], shell=True, stdout=subprocess.PIPE)
            ret = str(ret.stdout.read())
            alive = True
            ms = ret[ret.rindex('=') + 2:ret.rindex('ms')]
        except Exception as e:
            alive = False
            ms = 'unkown'
        print("ping {host} 完成，平均时间为{time}".format(host=host, time=ms))
        ret = {'host': host, 'url': url, 'time': ms, 'alive': alive}
        try:
            if(ret['alive'] is True and (self.__result is None or ret['time'] <= self.__result['time'])):
                self.__result = ret
                return self.__result
        except Exception as e:
            return ret

    def ping_list(self, urls):
        threads = []
        self.__result = None
        for url in urls:
            task = threading.Thread(target=self.ping, args=(url,))
            threads.append(task)
            task.start()
        for thread in threads:
            thread.join()
        print(self.__result)
        return self.__result['url']


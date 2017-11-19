import random;
import urllib;
import subprocess;
import re;
import urllib.request;
import socket;
class Visitor:
    '访问类'
    def __init(self):
        pass;
    def createIP(self):
        return "{}.{}.{}.{}".format(random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254)); 
    def getHost(self,url):
        return urllib.parse.urlparse(url).netloc
    def getHeaders(self,options={}):
        headers = {
            'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'X-Forwarded-For':self.createIP() ,
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'*',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'no-cache',
            'Connection':'keep-alive',
            'Cache-Control':'no-cache',
            'Pragma':'no-cache',
            'Upgrade-Insecure-Requests':'1'
        };
        if('host' in options):
            headers['host'] = options['host'];
        if('referer' in options):
            headers['referer'] = options['referer'];
        return headers;
    def visit(self,url,options={}):
        try:
            socket.setdefaulttimeout(10)
            request = urllib.request.Request(url,{},self.getHeaders(options));
            response = urllib.request.urlopen(request);
            print(response.read().decode('utf-8'));
            response.close();
        except Exception as e:
            print(e);
        pass; 
    def ping(self,url):
        try:
            ret = subprocess.Popen(["ping.exe", url],
                                   shell=True,
                                   stdout=subprocess.PIPE)
            ret = str(ret.stdout.read());
            alive = True;
            time = ret[ret.rindex('=')+2:ret.rindex('ms')]
        except Exception as e:
            alive = False;
            time = 'unkown';
        return {'time':time,'alive':alive};
a = Visitor().visit('https://announce.javbus2.pw/website.php');

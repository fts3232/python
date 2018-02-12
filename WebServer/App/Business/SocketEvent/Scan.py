import os
import re
import threading
from Business.JavBus import JavBus


class Scan():
    __options = None

    def __init__(self, options=None):
        self.__options = options

    def run(self, data=None):
        roots = ['E:\迅雷下载', 'D:\QQDownload', 'D:\Downloads']
        identifiers = []
        for root in roots:
            for path in os.listdir(root):
                temp = "{root}/{path}".format(root=root, path=path)
                ret = os.path.splitext(temp)
                if((os.path.isfile(temp) and ret[1].lower() in ['.avi', '.mp4']) or os.path.isdir(temp)):
                    ret = re.findall('([A-Za-z]{2,})-?(\d{3,4})(-\d+)?', path)
                    if(len(ret) > 0):
                        ret = ret[-1]
                        num = ret[1]
                        if(len(num) >= 4 and num[0] == '0' and ret[0] != 'heyzo'):
                            num = num[1:]
                        if(ret[2] != ''):
                            identifier = "{series}-{num}-{extra}".format(series=ret[0], num=num, extra=ret[2][1:])
                        else:
                            identifier = "{series}-{num}".format(series=ret[0], num=num)
                        ret = re.findall('\d{6,}', path)
                        if(len(ret) > 0):
                            identifier = path
                        identifiers.append(identifier)
        task = threading.Thread(target=self.threading, args=(identifiers,))
        task.start()

    def threading(self, identifiers):
        JavBus(self.__options['pool'], self.sendMessage).search(identifiers)

    def sendMessage(self, msg):
        self.__options['print']('scan', msg)

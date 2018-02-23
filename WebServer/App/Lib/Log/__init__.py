import os
import time


class Log():
    __config = {}

    def __init__(self, config):
        self.__config = config

    def write(self, data):
        today = time.strftime("%Y-%m-%d", time.localtime())
        filename = "{}.txt".format(today)
        path = self.__config['path']
        dirname = os.path.join(os.getcwd(), path)
        if(os.path.isdir(dirname) is False):
            os.mkdir(dirname)
        fo = open(os.path.join(dirname, filename), "a")
        data = "[{time}] {message} \n".format(time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), message=data)
        fo.write(data)
        fo.close()

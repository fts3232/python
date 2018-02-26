import os
import time


class File():

    __config = {}

    def __init__(self, config):
        self.__config = config

    def write(self, exception, exc_info):
        exc_type, exc_value, exc_tb = exc_info
        today = time.strftime("%Y-%m-%d", time.localtime())
        filename = "{}.txt".format(today)
        path = self.__config['path']
        dirname = os.path.join(os.getcwd(), path)
        if(os.path.isdir(dirname) is False):
            os.mkdir(dirname)
        fo = open(os.path.join(dirname, filename), "a")
        data = "[{time}] \n {type}:{error} \n file: {filename}:{lineno} \n text: {text} \n".format(time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), type=exc_type.__name__, error=exception.message, filename=exception.filename, lineno=exception.lineno, text=exception.text)
        fo.write(data)
        fo.close()

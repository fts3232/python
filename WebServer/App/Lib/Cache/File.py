import pickle
import hashlib
import os
import time


class File():
    __config = {}

    def __init__(self, config):
        self.__config = config

    def getStatus(self):
        return True

    def findFile(self, key):
        path = self.__config['path']
        md5 = hashlib.md5()
        md5.update(key.encode("utf-8"))
        filename = md5.hexdigest()
        if(os.path.isdir(path) is False):
            os.mkdir(path)
        return os.path.join(path, filename)

    def get(self, key):
        filepath = self.findFile(key)
        if(self.has(key) is True):
            fo = open(filepath, 'rb+')
            ret = fo.read()
            value = pickle.loads(ret)
            if(value['expire'] <= time.time()):
                self.delete(key)
                return False
            return value['data']
        else:
            return False

    def set(self, key, value, second=300, nx=False, xx=False):
        if(nx is True and self.has(key) is True):
            return False
        elif(xx is True and self.has(key) is False):
            return False
        filepath = self.findFile(key)
        value = {'data': value, 'expire': time.time() + second}
        fo = open(filepath, 'wb+')
        fo.write(pickle.dumps(value))
        fo.close()
        return True

    def setnx(self, key, value, second=300):
        return self.set(key, value, second, nx=True)

    def has(self, key):
        filepath = self.findFile(key)
        return os.path.isfile(filepath)

    def delete(self, key):
        filepath = self.findFile(key)
        return os.remove(filepath)

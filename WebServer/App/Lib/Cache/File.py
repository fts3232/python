import pickle
import hashlib
import os
import time
from .Factory import Factory


class File(Factory):

    def findFile(self, key):
        path = self._config['path']
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

    def set(self, key, value, second=300):
        filepath = self.findFile(key)
        value = {'data': value, 'expire': time.time() + second}
        fo = open(filepath, 'wb+')
        fo.write(pickle.dumps(value))
        fo.close()
        return True

    def has(self, key):
        filepath = self.findFile(key)
        return os.path.isfile(filepath)

    def delete(self, key):
        filepath = self.findFile(key)
        return os.remove(filepath)

import redis
from .Factory import Factory


class Redis(Factory):
    __instance = None

    def __init__(self, config):
        Factory.__init__(self)
        self.__instance = redis.Redis(host=config['host'], port=config['port'], db=config['db'])
        self.__instance.ping()

    def get(self, key):
        return self.__instance.get(key)

    def set(self, key, value, second=300, nx=False, xx=False):
        return self.__instance.set(key, value, ex=second, nx=nx, xx=xx)

    def setnx(self, key, value, second=300):
        return self.set(key, value, second, nx=True)

    def has(self, key):
        return self.exists(key)

    def delete(self, key):
        return self.delete(key)

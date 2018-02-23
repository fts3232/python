import redis


class Redis():
    __instance = None
    __status = False

    def __init__(self, config):
        self.__instance = redis.Redis(host=config['host'], port=config['port'], db=config['db'])
        try:
            self.__instance.ping()
            self.__status = True
        except Exception as e:
            self.__status = False

    def getStatus(self):
        return self.__status

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

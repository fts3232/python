import importlib
import os


class Cache():
    __config = {}
    __instance = None

    def __init__(self, config):
        try:
            self.__config = config
            self.load(config['driver'])
        except Exception as e:
            print("Cache驱动：{}-加载失败 错误：{}".format(config['driver'], str(e)))
            self.load('File')

    def load(self, driver):
        config = self.__config
        config = config[driver]
        dirname = os.path.dirname(__file__)
        filename = "{}.py".format(driver)
        if(os.path.isfile(os.path.join(dirname, filename)) is False):
            raise Exception("Cache驱动：{}-不存在".format(driver))
        if(__name__ != '__main__'):
            namespace = __name__ + '.' + driver
        else:
            namespace = driver
        module = importlib.import_module(namespace)
        obj = getattr(module, driver)
        self.__instance = obj(config)
        print("Cache驱动：{}-加载成功".format(driver))

    def __getattr__(self, funcname):
        if(hasattr(self.__instance, funcname)):
            return getattr(self.__instance, funcname)
        return False

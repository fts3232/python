import importlib


class Container():
    __instances = {}

    def make(self, name):
        if(name in self.__instances):
            return self.__instances[name]
        else:
            return False
        pass

    # 每解析一次实例化一次
    def bind(self, name, obj):
        if(isinstance(obj, str)):
            self.__instances[name] = importlib.import_module(obj)
        elif(obj.__name__ == '<lambda>'):
            self.__instances[name] = lambda self: obj(self)
        elif(hasattr(obj, '__name__')):
            self.instance(name, obj)

    # 只实例化一次
    def singleton(self, name, obj):
        if(isinstance(obj, str)):
            self.__instances[name] = importlib.import_module(obj)
        elif(obj.__name__ == '<lambda>'):
            self.__instances[name] = obj(self)
        elif(hasattr(obj, '__name__')):
            self.instance(name, obj)

    # 绑定实例
    def instance(self, name, obj):
        self.__instances[name] = obj

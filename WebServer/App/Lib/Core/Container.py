import importlib


class Container():
    __instances = {}

    def make(self, name):
        try:
            obj = False
            if(name not in self.__instances):
                raise('instance不存在')
            instance = self.__instances[name]
            if(instance['obj'] is not None and instance['type'] == 'singleton'):
                obj = instance['obj']
            else:
                if(instance['register'] == 'module'):
                    obj = importlib.import_module(instance['value'])
                elif(instance['register'] == 'function'):
                    obj = instance['value'](self)
                if(instance['type'] == 'singleton'):
                    self.__instances[name]['obj'] = obj
        except Exception as e:
            obj = False
        return obj

    # 每解析一次实例化一次
    def bind(self, name, obj):
        if(isinstance(obj, str)):
            self.__instances[name] = {'obj': None, 'value': obj, 'register': 'module', 'type': 'bind'}
            # importlib.import_module(obj)
        elif(obj.__name__ == '<lambda>'):
            self.__instances[name] = {'obj': None, 'value': obj, 'register': 'function', 'type': 'bind'}
            # lambda self: obj(self)
        elif(hasattr(obj, '__name__')):
            self.instance(name, obj)

    # 只实例化一次
    def singleton(self, name, obj):
        if(isinstance(obj, str)):
            self.__instances[name] = {'obj': None, 'value': obj, 'register': 'module', 'type': 'singleton'}
            # importlib.import_module(obj)
        elif(obj.__name__ == '<lambda>'):
            self.__instances[name] = {'obj': None, 'value': obj, 'register': 'function', 'type': 'singleton'}
            # obj(self){'obj': None, 'module': obj}
        elif(hasattr(obj, '__name__')):
            self.instance(name, obj)

    # 绑定实例
    def instance(self, name, obj):
        self.__instances[name] = {'obj': obj, 'value': obj, 'register': 'instance', 'type': 'singleton'}

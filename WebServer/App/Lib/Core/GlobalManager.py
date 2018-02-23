def init():
    global __global
    __global = {}


def set(name, value):
    name = name.lower()
    __global[name] = value


def get(name):
    name = name.lower()
    try:
        return __global[name]
    except Exception:
        print(name + '参数不存在')


def has(name):
    name = name.lower()
    return name in __global


def remove(name):
    name = name.lower()
    __global.pop(name)

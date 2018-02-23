# from . import DB
# from . import DM5
# from . import HKPic
# from . import JavBus
# from . import Live
# from . import WebServer
# DB = DB.config
# DM5 = DM5.config
# HKPic = HKPic.config
# JavBus = JavBus.config
# Live = Live.config
# WebServer = WebServer.config
import os
import importlib


def load():
    global config
    config = {}
    dirname = os.path.join(os.getcwd(), 'App\Config')
    files = os.listdir(dirname)
    for x in files:
        if(os.path.isfile(os.path.join(dirname, x)) and x != '__init__.py'):
            (filename, extension) = os.path.splitext(x)
            config[filename] = importlib.import_module('Config.' + filename).config
            print(filename + '配置文件加载完成')


def get(name):
    try:
        return config[name]
    except Exception:
        print(name + '配置文件不存在')

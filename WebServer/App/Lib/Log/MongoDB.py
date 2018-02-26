from mongoengine import *
import datetime


class Log(Document):
    TYPE = StringField(required=True)
    ERROR = StringField(required=True)
    FILE = StringField(required=True)
    LINE = IntField(required=True)
    TEXT = StringField(required=True)
    CREATED_TIME = DateTimeField(default=datetime.datetime.now)


class MongoDB():

    __config = {}
    __collection = None
    __db = None

    def __init__(self, config):
        self.__config = config
        connect(self.__config['db'], host=self.__config['host'], port=self.__config['port'])

    def write(self, exception, exc_info):
        exc_type, exc_value, exc_tb = exc_info
        p = Log(TYPE=exc_type.__name__, ERROR=exception.msg, FILE=exception.filename, LINE=exception.lineno, TEXT=exception.text)
        p.save()

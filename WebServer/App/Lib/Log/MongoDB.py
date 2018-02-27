from mongoengine import *
import datetime
import traceback
from .Factory import Factory


class Log(Document):
    TYPE = StringField(required=True)
    ERROR = StringField(required=True)
    FILE = StringField(required=True)
    LINE = IntField(required=True)
    SOURCE = StringField(required=True)
    FUNCNAME = StringField(required=True)
    CREATED_TIME = DateTimeField(default=datetime.datetime.now)


class MongoDB(Factory):

    __collection = None
    __db = None

    def __init__(self, config):
        Factory.__init__(config)
        connect(self._config['db'], host=self._config['host'], port=self._config['port'])

    def write(self, exc_info):
        exc_type, exc_value, exc_tb = exc_info
        tb = traceback.extract_tb(exc_tb)
        (filename, linenum, funcname, source) = tb[-1]
        p = Log(TYPE=exc_type.__name__, ERROR=str(exc_value), FILE=filename, LINE=linenum, SOURCE=source, FUNCNAME="{}()".format(funcname))
        p.save()

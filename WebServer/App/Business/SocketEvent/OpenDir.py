import subprocess
import os
from Business.Av import Av


class OpenDir():
    __options = None

    def __init__(self, options=None):
        self.__options = options

    def run(self):
        try:
            msg = '打开成功'
            ret = Av(self.__options['app'].make('Config').get('Av')).scanLocalFolder(self.__options['data'])
            if(ret is False):
                raise Exception('文件夹不存在')
            ret = subprocess.Popen('explorer "{path}"'.format(path=os.path.dirname(ret[self.__options['data']]['path'])), shell=True)
        except Exception as e:
            msg = '打开失败'
            print(e)
        self.__options['print']('openDir', msg)

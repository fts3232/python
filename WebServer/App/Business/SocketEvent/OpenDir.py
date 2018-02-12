import subprocess
import os
from Helpers.functions import findMovie


class OpenDir():
    __options = None

    def __init__(self, options=None):
        self.__options = options

    def run(self):
        try:
            msg = '打开成功'
            roots = ['E:\迅雷下载', 'D:\QQDownload', 'D:\Downloads']
            ret = findMovie(roots, self.__options['data'], ['.avi', '.mp4'])
            if(ret is None):
                raise Exception('文件夹不存在')
            ret = subprocess.Popen('explorer "{path}"'.format(path=os.path.dirname(ret)), shell=True)
        except Exception as e:
            msg = '打开失败'
            print(e)
        self.__options['print']('openDir', msg)

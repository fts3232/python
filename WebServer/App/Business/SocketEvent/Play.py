import subprocess
from Helpers.functions import findMovie


class Play():
    __options = None

    def __init__(self, options=None):
        self.__options = options

    def run(self):
        try:
            msg = '播放成功'
            roots = ['E:\迅雷下载', 'D:\QQDownload', 'D:\Downloads']
            ret = findMovie(roots, self.__options['data'], ['.avi', '.mp4'])
            if(ret is None):
                raise Exception('文件不存在')
            ret = subprocess.Popen('"{path}"'.format(path=ret), shell=True)
        except Exception as e:
            msg = '播放失败'
            print(e)
        self.__options['print']('play', msg)

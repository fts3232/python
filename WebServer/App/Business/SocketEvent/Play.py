import subprocess
from Business.Av import Av


class Play():
    __options = None

    def __init__(self, options=None):
        self.__options = options

    def run(self):
        try:
            msg = '播放成功'
            ret = Av(self.__options['app'].make('Config').get('Av')).scanLocalFolder(self.__options['data'])
            if(ret is False):
                raise Exception('文件不存在')
            ret = subprocess.Popen('"{path}"'.format(path=ret), shell=True)
        except Exception as e:
            msg = '播放失败'
            print(e)
        self.__options['print']('play', msg)

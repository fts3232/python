import os
import time
import traceback
from .Factory import Factory


class File(Factory):

    def write(self, exc_info):
        exc_type, exc_value, exc_tb = exc_info
        tb = traceback.extract_tb(exc_tb)
        today = time.strftime("%Y-%m-%d", time.localtime())
        filename = "{}.txt".format(today)
        path = self._config['path']
        dirname = os.path.join(os.getcwd(), path)
        if(os.path.isdir(dirname) is False):
            os.mkdir(dirname)
        fo = open(os.path.join(dirname, filename), "a")
        data = "[{time}] \n {type}:{error} \n ".format(time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), type=exc_type.__name__, error=exc_value)
        (filename, linenum, funcname, source) = tb[-1]
        data = data + "file: {filename}:{lineno} {text} in {funcname}() \n\n".format(filename=filename, lineno=linenum, text=source, funcname=funcname)
        fo.write(data)
        fo.close()

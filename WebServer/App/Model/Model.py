from Lib.Core import GlobalManager


class Model():
    _db = None

    def __init__(self):
        if(GlobalManager.has('DBConn')):
            self._db = GlobalManager.get('DBConn')
        else:
            self._db = GlobalManager.get('ConnectionPool').conn()
            GlobalManager.set('DBConn', self._db)
        pass

    def __del__(self):
        if(GlobalManager.has('DBConn')):
            db = GlobalManager.get('DBConn')
            db.release()
            GlobalManager.remove('DBConn')

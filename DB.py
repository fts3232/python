import sqlite3


class DB:
    'DB'
    __conn = None
    __cursor = None

    def __init__(self):
        try:
            self.__conn = sqlite3.connect('./JavBus/db.db')
            print("链接数据库成功")
            self.__cursor = self.__conn.cursor()
        except Exception:
            print("链接数据库失败")

    def __del__(self):
        if(self.__conn is not None):
            self.__conn.close()

    def select(self, sql, param=[]):
        self.__cursor.execute(sql, param)
        return self.__cursor.fetchall()

    def update(self, sql, param=[]):
        self.__cursor.execute(sql, param)
        return self.__conn.rowcount

    def delete(self, sql, param=[]):
        self.__cursor.execute(sql, param)
        return self.__conn.rowcount

    def insert(self, sql, param=[]):
        self.__cursor.execute(sql, param)
        return self.__cursor.rowcount

    def query(self, sql, param=[]):
        self.__cursor.execute(sql, param)

    def commit(self):
        self.__conn.commit()
        pass

    def rollback(self):
        self.__conn.rollback()
        pass

    def createTable(self):
        sql = "CREATE TABLE IF NOT EXISTS RECORD(\
               ID INTEGER PRIMARY KEY,\
               IDENTIFIER VCHAR(10) NOT NULL,\
               NAME  TEXT NOT NULL,\
               SAMPLE tinyint(1) NOT NULL DEFAULT 0,\
               MAGNET tinyint(1) NOT NULL DEFAULT 0,\
               CREATED_TIME DATETIME DEFAULT (datetime('now','localtime'))\
               );"
        self.query(sql)
        ret = self.__cursor.rowcount
        if(ret == 0):
            print('创建数据库成功')
        else:
            print('创建数据库失败')
        self.commit()
        pass

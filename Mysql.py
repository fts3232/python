import pymysql
import re


class Mysql:
    'Mysql'
    __conn = None
    __cursor = None

    def __init__(self):
        try:
            self.__conn = pymysql.connect("localhost", "root", "", "JavBus", charset="utf8")
            self.__cursor = self.__conn.cursor(cursor=pymysql.cursors.DictCursor)
            print("链接数据库成功")
        except Exception as e:
            print("链接数据库失败: " + repr(e))

    def __del__(self):
        if(self.__conn is not None):
            self.__conn.close()
            self.__cursor.close()

    def select(self, sql, param=[]):
        sql, param = self.perpare(sql, param)
        self.__cursor.execute(sql, param)
        return self.__cursor.fetchall()

    def find(self, sql, param=[]):
        sql, param = self.perpare(sql, param)
        self.__cursor.execute(sql, param)
        return self.__cursor.fetchone()

    def count(self, sql, param=[]):
        sql, param = self.perpare(sql, param)
        self.__cursor.execute(sql, param)
        row = self.__cursor.fetchone()
        return list(row.values())[0]

    def update(self, sql, param=[]):
        sql, param = self.perpare(sql, param)
        self.__cursor.execute(sql, param)
        return self.__cursor.rowcount

    def delete(self, sql, param=[]):
        sql, param = self.perpare(sql, param)
        self.__cursor.execute(sql, param)
        return self.__cursor.rowcount

    def perpare(self, sql, param=[]):
        if(len(param) == 0):
            return sql, param
        pattern = re.compile(r':\w+')
        ret = pattern.findall(sql)
        if(len(ret) == 0):
            return sql, param
        sql = pattern.sub('%s', sql)
        tempParam = []
        for x in ret:
            tempParam.append(param[x[1:]])
        return sql, tempParam

    def insert(self, sql, param=[]):
        sql, param = self.perpare(sql, param)
        self.__cursor.execute(sql, param)
        return self.__conn.insert_id()

    def query(self, sql, param=[]):
        sql, param = self.perpare(sql, param)
        self.__cursor.execute(sql, param)

    def commit(self):
        self.__conn.commit()

    def rollback(self):
        self.__conn.rollback()

    def begin(self):
        self.__conn.begin()

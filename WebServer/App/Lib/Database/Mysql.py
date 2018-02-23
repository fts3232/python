# coding: utf8
import pymysql
import re


class ConnectionPool:
    __pool = []
    __free_pool = []
    __max_connection = 10
    __min_connection = 2
    __total_connection = 0
    __config = None

    def __init__(self, config):
        self.__config = config
        self.__max_connection = config['max_connection'] if('max_connection' in config) else 10
        self.__min_connection = config['min_connection'] if('min_connection' in config) else 2
        for x in range(self.__min_connection):
            conn = Connection(config)
            self.__pool.append(conn)
            pass
        print('连接池创建成功')

    def conn(self):
        for conn in self.__pool:
            if(conn.is_busy() is False):
                conn.set_busy(True)
                print('获取链接成功')
                return conn
        if(len(self.__pool) < self.__max_connection):
            conn = Connection(self.__config)
            conn.set_busy(True)
            self.__pool.append(conn)
            print('获取链接成功')
            return conn
        else:
            print('没有可用的链接')
            return None

    def close(self):
        for conn in self.__pool:
            conn.close()
        print('关闭连接池')


class Connection():

    'Mysql-Connection'
    __conn = None
    __cursor = None
    __busy = False

    def __init__(self, config):
        try:
            self.__conn = pymysql.connect(config['host'], config['user'], config['password'], config['db'], charset=config['charset'])
            self.__cursor = self.__conn.cursor(cursor=pymysql.cursors.DictCursor)
            print("数据库链接成功")
        except Exception as e:
            print("数据库链接失败: " + repr(e))

    def select(self, sql, param={}):
        sql, param = self.perpare(sql, param)
        self.__cursor.execute(sql, param)
        return self.__cursor.fetchall()

    def find(self, sql, param={}):
        sql, param = self.perpare(sql, param)
        self.__cursor.execute(sql, param)
        return self.__cursor.fetchone()

    def count(self, sql, param={}):
        sql, param = self.perpare(sql, param)
        self.__cursor.execute(sql, param)
        row = self.__cursor.fetchone()
        return list(row.values())[0]

    def update(self, sql, param={}):
        sql, param = self.perpare(sql, param)
        self.__cursor.execute(sql, param)
        return self.__cursor.rowcount

    def delete(self, sql, param={}):
        sql, param = self.perpare(sql, param)
        self.__cursor.execute(sql, param)
        return self.__cursor.rowcount

    def perpare(self, sql, param={}):
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

    def set_busy(self, status):
        self.__busy = status

    def is_busy(self):
        return self.__busy is True

    def close(self):
        self.__conn.close()
        self.__cursor.close()
        print('关闭链接')

    def release(self):
        print('释放链接')
        self.set_busy(False)


# config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '',
#     'db': 'JavBus',
#     'charset': 'utf8'
# }
# pool = ConnectionPool(config)
# conn1 = pool.conn()
# conn2 = pool.conn()
# conn3 = pool.conn()
# conn4 = pool.conn()
# conn5 = pool.conn()
# conn6 = pool.conn()
# conn7 = pool.conn()
# conn8 = pool.conn()
# conn9 = pool.conn()
# conn10 = pool.conn()
# conn11 = pool.conn()
# conn1.release()
# conn12 = pool.conn()
# print(conn1.select('select * from MOVIE'))
# pool.close()

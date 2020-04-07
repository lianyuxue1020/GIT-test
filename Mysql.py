from pymysql import *
import time
from threading import Lock

class Mysql_Python:
    '''
    类声明: 自定义pymysql类方法
    '''
    def __init__(self, database,
                 host='localhost',
                 user='root',
                 password='123456',
                 port=3306,
                 charset='utf8'):
        '''
        方法声明: 连接数据库参数
        :param database: 库
        :param host: 主机
        :param user: 用户
        :param password: 密码
        :param port: 端口
        :param charset: 字符集
        '''
        self.__host = host
        self.__user = user
        self.__password = password
        self.__port = port
        self.__database = database
        self.__charset = charset
        self.__lock = Lock()


    def open(self):
        """
        方法声明: 连接数据库
        :return: "连接成功"
        """
        try:
            self.__db = connect(host=self.__host,
                              port=self.__port,
                              user=self.__user,
                              password=self.__password,
                              database=self.__database,
                              charset=self.__charset)
            self.__cur = self.__db.cursor()
            # self.__db.ping(True)
            return "连接成功"
        except Exception as err:
            return err



    def close(self):
        '''
        方法声明: 关闭连接
        :return:
        '''
        self.__cur.close()
        self.__db.close()

    def idu(self, sql, L=[]):
        '''
        方法声明: insert， delete， update
        :param sql: 执行语句
        :param L: sql参数
        :return: True/False
        '''
        try:
            # self.__lock.acquire()
            self.__cur.execute(sql, L)
            # self.__lock.release()
            return True
        except Exception as err:
            print('错误:', err)
            # self.__lock.release()
            return False

    def sall(self, sql, L=[]):
        '''
        方法声明: select
        :param sql: 执行语句
        :param L: sql参数
        :return:
        '''
        try:
            self.__lock.acquire()
            self.__cur.execute(sql, L)
            self.__lock.release()
            result = self.__cur.fetchall()
            return result
        except Exception as err:
            # print('错误:', err)
            self.__lock.release()

    def commit(self):
        '''
        方法声明: commit提交事件
        :return: "提交成功"
        '''
        try:
            self.__db.commit()
            # print("提交成功")
        except Exception as err:
            self.__db.rollback()
            print('错误，已回滚:', err)



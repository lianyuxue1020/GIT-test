from Mysql import Mysql_Python as mydb
from threading import Lock

def Connect():
    '''
    方法声明: 数据库连接配置功能
    :return: 数据库连接对象，连接状态
    '''
    # 机房测试数据库
    # db = mydb(host='10.10.50.3', user='skdata', password='Xx6%0e!s', port=3306, database='skdata')

    # 公司测试数据库
    db = mydb(host='172.16.8.2', user='root', password='123456', port=3306, database='index_fpqqlsh')
    status = db.open()
    return db, status
import time
from threading import Lock

# 插入数据
class Insert_Data():
    """
    类声明: 数据插入数据库

    """
    def __init__(self, db):
        """
        方法声明: 初始化数据库连接
        参数:
        :param db: 数据连接池
        """
        self.__db = db

    def __Insert_Fpqqlsh(self, fpqqlsh, log_data):
        """
        方法声明: 插入数据库dj_fpqqlsh
        参数:
        :param fpqqlsh: 发票请求流水号字段数据
        :param log_data: log报文字段数据
        :return:
        """

        __select_time = time.time()
        __SQL = "insert into dj_fpqqlsh (fpqqlsh,select_time,log) values (%s, from_unixtime(%s), %s)"
        __args = [fpqqlsh, __select_time, log_data]
        self.__db.idu(__SQL, __args)

    def __Insert_Status(self, name, count, state, start_time, end_time, upload):
        """
        方法声明: 插入数据库message_status
        :param name: 名称
        :param count: 数量
        :param state: 状态
        :param start_time: 开始时间
        :param end_time: 结束时间
        :param upload: 未定义
        :return:
        """
        __SQL = "insert into message_status (name, count, state, start_time, end_time, upload) values " \
                "(%s, %s, %s, from_unixtime(%s), from_unixtime(%s), %s)"
        __args = [name, count, state, start_time, end_time, upload]
        req = self.__db.idu(__SQL, __args)
        if req:
            self.__db.commit()
    def select(self, fpqqlsh):
        __SQL = "select fpqqlsh,log from dj_fpqqlsh where fpqqlsh=%s"
        data = self.__db.sall(__SQL, L=[fpqqlsh])
        return data
    def run(self,queue):
        """
        方法声明:  运行数据
        参数:
        :param message:
        :param queue: 队列
        :return:
        """
        # 记录get获取数量
        commit = 0
        while True:
            try:
                data = queue.get()
                if data[0] == "FPQQLSH":
                    self.__Insert_Fpqqlsh(data[1],data[2])
                    commit += 1
                    if commit == 1000 or queue.qsize() < 100:
                        self.__db.commit()
                        commit = 0
                elif data[0] == "STATUS":
                    name = data[1]['name']
                    count = data[1]['count']
                    state = data[1]['state']
                    start_time = data[1]['start_time']
                    end_time = data[1]['end_time']
                    upload = data[1]['upload']
                    self.__Insert_Status(name,count,state,start_time,end_time,upload)

            except:
                print("异常退出")
                break



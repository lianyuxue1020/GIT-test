import threading
import os

class Thread(threading.Thread):
    """
    类声明: 自定义多线程
    """
    def __init__(self, func, args=(), kwargs={}):
        """
        方法声明: 重写Thread方法
        :param func: 运行函数
        :param args:
        :param kwargs:
        """
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        '''
        方法声明: 重写run方法
        :return:
        '''
        # print("开始子进程:", self.name)
        # print("子线程PID:", os.getppid())
        self.func(*self.args, **self.kwargs)

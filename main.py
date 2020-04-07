# -*- coding: utf-8 -*-
from Definition_Connect import Connect
from Definition_Thread import Thread
from Definition_GetMessage import FileMessage
from Definition_Inset import Insert_Data
from multiprocessing import Queue
import os,sys
import  threading

def main():
    '''
    方法声明: 报文提取主程序
    :return:
    '''
    print("主线程PID:",os.getpid())

    # 数据库连接
    db,status = Connect()
    if status == "连接成功":
        print(status)
    else:
        print(status)
        print("已退出程序")
        sys.exit(0)

    # Windows环境
    # files = [r'C:\Users\Administrator\Desktop\分析日志\catalina.2020-02-10.out\catalina.2020-02-10.out',
    #          r'C:\Users\Administrator\Desktop\分析日志\catalina.2020-03-20.out.bak\catalina.2020-03-20.out.bak',
    #          r'C:\Users\Administrator\Desktop\分析日志\catalina.2019-08-13.out',
    #          r'C:\Users\Administrator\Desktop\分析日志\catalina.2019-10-23.out',
    #          r'C:\Users\Administrator\Desktop\分析日志\catalina.out.02.10_21_00-21_30.log']

    # Linux环境
    # files = [r'/app/python/test/catalina.2020-03-20.out',
    #          r'/app/python/test/catalina.2020-03-17.out',
    #          r'/app/python/test/catalina.2019-08-13.out',
    #          r'/app/python/test/catalina.2020-02-20.out']

    # files = [r'/app/python/test/catalina.2019-08-13.out',
    #          r'/app/python/test/catalina.2019-11-14.out',
    #          r'/app/python/test/catalina.2020-02-20.out',
    #          r'/app/python/test/catalina.2020-03-17.out',
    #          r'/app/python/test/catalina.2020-03-18.out',
    #          r'/app/python/test/catalina.2020-03-19.out',
    #          r'/app/python/test/catalina.2020-03-20.out',
    #          r'/app/python/test/catalina.2020-03-21.out',
    #          r'/app/python/test/catalina.2020-03-22.out']

    # files = [r'/app/python/test/catalina.2020-03-20.out',
    #          r'/app/python/test/catalina.2020-02-20.out',]

    # 多线程运行任务
    message = FileMessage()

    # 消息队列
    queue = Queue(1000)
    print("队列开启")
    insert = Insert_Data(db)
    t2 = Thread(func=insert.run, args=(queue,))
    t2.setDaemon(True)
    t2.start()
    while True:
        print("-----------------")
        print(" 1.分析文件       ")
        print(" 2.查看状态       ")
        print(" 3.查看线程       ")
        print(" 4.查看报文       ")
        print("【quit退出】      ")
        print("-----------------")
        try:
            command = input("输入指令:")
            if command == '1':
                file = input("请输入录入文件路径:")
                if not file:
                    continue
                t1 = Thread(func=message.Open, args=(file.strip(), queue))
                t1.setDaemon(True)
                t1.start()
            elif command == '2':
                if message.Statues():
                    for i in message.Statues():
                        print(i)
                else:
                    print("无查询数据")
            elif command == '3':
                print(threading.enumerate())
            elif command == '4':
                fpqqlsh = input("请输入流水号:")
                data = insert.select(fpqqlsh.strip())
                if data:
                    mag = data[0][0]
                    log = data[0][1]
                    print("流水号:{}\n".format(mag),log)
                else:
                    print("没有该流水号信息")
            elif command == 'quit':
                break
            else:
                print("指令错误!")
        except KeyboardInterrupt:
            print("异常退出")
            sys.exit(0)

        """
        /app/python3.8/lib/python3.8/site-packages/pymysql/cursors.py:170: Warning: (1366, "Incorrect string value: '\\xE3\\x83\\xBB\\xE9\\x9F\\xB6...' for column 'log' at row 1")
          result = self._query(query)
        /app/python3.8/lib/python3.8/site-packages/pymysql/cursors.py:170: Warning: (1265, "Data truncated for column 'log' at row 1")
          result = self._query(query)
        """

if __name__ == '__main__':
    main()
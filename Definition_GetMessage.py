import time, datetime
import re
import chardet

"""
chardet: 推断编码方式
"""

class FileMessage():
    """
    类声明: 文件分析类
    """
    def __init__(self):
        """
        方法声明: 初始化文件路径
        :param file: 文件路径
        """
        # 数据状态存储属性
        self.__status = []

    def Open(self, file, queue):
        """
        方法声明: 打开文件，分析报文信息
        :return:
        """
        try:
            with open(file, 'rb') as src:
                read = src.read(1024)
                read_decode = chardet.detect(read)['encoding']
                print("\n编码:{}".format(read_decode))
                src.seek(0)
                # 开始记录耗时
                start_time = datetime.datetime.now()
                print("\n开始时间:{}".format(start_time))
                # 报文拼接
                datas = ''
                # 数据状态
                status = False
                # 数据结构
                info = {'name': file,
                             'count': 0,
                             'state': True,
                             'start_time':  int(time.mktime(start_time.timetuple())),
                             'end_time': 'null',
                             'upload': 0.0}
                self.__status.append(info)
                while True:
                    readline = src.readline().decode(encoding=read_decode, errors='ignore')
                    if not readline:
                        end_time = datetime.datetime.now()
                        time_cost = end_time - start_time
                        info['state'] = False
                        info['end_time'] = int(time.mktime(end_time.timetuple()))
                        mag = "STATUS"
                        queue.put((mag, info))
                        print("\n{}条记录".format(info['count']))
                        print("耗时:{}".format(time_cost))
                        break
                    if re.findall(r"<business id='FPKJ' comment='发票开具'>", readline):
                        # 获取流水号
                        fpqqlsh = re.search(r'<FPQQLSH>(\w{20})</FPQQLSH>', readline).group(1)
                        datas += readline
                        status = True
                        continue
                    if status:
                        datas += readline
                    if re.findall('</COMMON_FPKJ_XMXXS></REQUEST_COMMON_FPKJ></business>', readline):
                        mag = "FPQQLSH"
                        queue.put((mag, fpqqlsh, datas))
                        info['count'] += 1
                        status = False
                        datas = ''
        except FileNotFoundError as err:
            print("文件打开错误:", err)
        except OSError as err1:
            print("错误", err1)

    def Statues(self):
        '''
        方法声明:  获取数据组状态方法
        :return: 数据组列表状态信息
        '''
        return self.__status

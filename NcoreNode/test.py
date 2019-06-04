# import socket
# print(socket.gethostbyname(socket.getfqdn(socket.gethostname())))

import os, sys
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# def write_pickle(data):
#
#     output = open(BASE_DIR + '/NcoreNode/config/data.pk', 'wb')
#     pickle.dump(data, output)
#     output.close()
#
# def read_pickle():
#
#     pkl_file = open(BASE_DIR + '/NcoreNode/config/data.pk', 'rb')
#     data = pickle.load(pkl_file)
#
#     pkl_file.close()
#     return data
#
# class NCOREPICKLE(object):
#
#     def __init__(self):
#
#         self.input = open(BASE_DIR + '/NcoreNode/config/data.pk', 'rb')
#
#     def write_pickle(self, data):
#         output = open(BASE_DIR + '/NcoreNode/config/data.pk', 'wb')
#         pickle.dump(data, output)
#         output.close()
#
#     def read_pickle(self):
#         data = pickle.load(self.input)
#         self.input.close()
#         return data

# npicket = NCOREPICKLE()
#
# npicket.write_pickle('changhao - pickle')
# print(npicket.read_pickle())

# print(read_pickle())
# write_pickle('sssss')

#
# from tools.ncoretool import parser_query_uuid, parser_query_keyid, parser_write_uuid, parser_query_server, parser_query_port, NCOREPICKLE
#
# aa = NCOREPICKLE()
# print(aa.read_pickle())


# import os
#
# print(os.cpu_count())


# import os, time
# from multiprocessing import Process
#
#
# def worker():
#     print("子进程执行中>>> pid={0},ppid={1}".format(os.getpid(), os.getppid()))
#     time.sleep(2)
#     print("子进程终止>>> pid={0}".format(os.getpid()))
#
#
# if __name__ == '__main__':
#     print("主进程执行中>>> pid={0}".format(os.getpid()))
#
#     ps = []
#     # 创建子进程实例
#     for i in range(2):
#         p = Process(target=worker, name="worker" + str(i), args=())
#         ps.append(p)
#
#     # 开启进程
#     for i in range(2):
#         ps[i].start()


#
# from tools.queryTicket import Ticketquery
#
# aa = Ticketquery()
# print(aa.query('北京', '上海', '2019-06-20'))


# for i in range(1, 11):
#     print(i)

count = []
a = []
count.append(a)

print(count)
print(len(count))





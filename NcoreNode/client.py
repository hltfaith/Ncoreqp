#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import struct
import schedule
from multiprocessing import Process, Pool
import threading

from pycrypto import encrypt
from tools.ncoretool import parser_query_uuid, parser_query_keyid, parser_write_uuid, parser_query_server,\
    parser_query_port, NCOREPICKLE, data_convert, TASKOK
from tools.queryTicket import Ticketquery

'''

    1. 120 seconds Task
    2. 
    
    服务端
        0. 两个进程
            1.定时进程
                1. 清理取消的车票
                2. 清理数据库加密key帐号
                3. 定时任务-10分钟清理数据库
            2.服务进程
    
        1. 判断是否激活，分配id
    
    客户端
        页面： 1. 认证  2.加密码  3. ip add  4. 端口
        
        1. 首次激活，获得id
        2. 机制：客户端发起无id号数据包，服务端分配id号同时写入数据库，时间有效期10分钟，间隔时间5秒，
            客户端每五秒写入；
        
'''

def socketStart(msg):

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(15)

        server = str(parser_query_server())
        port = int(parser_query_port())
        server_ip_port = (server, port)

        client.connect(server_ip_port)
        sendPack(msg, client)
        client.close()

    except ConnectionRefusedError:
        print('【 警告 】 服务器连接失败.....')

def unpack(data):

    '''
    获取头信息
    :return:
    '''

    try:
        db = eval(data)

        # 解包 判断初次发包,  建立服务器连接
        if db['id'] != '' and db['status'] == 'ack':
            print('初次收包')
            ack_data = db

            # uuid写入conf文件
            parser_write_uuid(db['id'])

        # 判断返回进度包
        # elif db['key'] == '101010' and db['status'] == 'qpsuccess':
        #     pass

        # 再次获取执行任务
        elif db['key'] == parser_query_keyid() and db['type'] == 'push_task':
            print('获取任务')
            ack_data = db

            # 序列化存储 - 服务端任务列表
            ncorepickle = NCOREPICKLE()
            ncorepickle.write_pickle(db['data'])

            # for i in db['data']:
            #     print(i)

        # 再次获取执行任务
        elif db['key'] == parser_query_keyid() and db['type'] == 'delete_task':
            print('清空task-ok.pk文件')

            data = {('', '', '', '', '')}

            ok = TASKOK()
            ok.write_pickle(data)

        else:
            print('未识别的数据包!!!')

    except Exception:
        pass

    return ack_data

def sendPack(msg, client):

    '''

        发包功能

    :return:
    '''

    try:

        # 发请求包
        # 包头大小
        cmd_msg_len = len(msg)
        msg_len_stru = struct.pack('i', cmd_msg_len)

        client.send(msg_len_stru)
        client.sendall(bytes(str(msg), encoding='utf-8'))

        # 接收包, 解决粘包
        from_server_msglen = client.recv(4)
        unpack_len_msg = struct.unpack("i", from_server_msglen)[0]

        recv_msg_len = 0
        all_msg = b""
        while recv_msg_len < unpack_len_msg:
            every_recv_date = client.recv(1024)
            all_msg += every_recv_date              # 将每次接收到的数据进行拼接和统计
            recv_msg_len += len(every_recv_date)    # 对每次接受到的数据进行累加

        data = all_msg.decode("utf-8")

        print(unpack(data))

    except socket.timeout as e:
        print('socket timeout .....')

    except Exception:
        pass

def client_exec_task1():

    '''
    执行
    :return:
    '''

    # print("判断keyid是否为空")
    if parser_query_keyid() == '':
        exit('ERROR: [key码为空! 运行失败!]')

    msg0 = {
        'key': encrypt(str(1111111)),
        'id': str(parser_query_uuid()),
        'status': 'syn',
        'address': '',
        'type': '',
        'length': '',
        'data': ''
    }

    msg1 = {
        'key': encrypt(str(parser_query_keyid())),
        'id': str(parser_query_uuid()),
        'status': 'syn',
        'address': '',
        'type': '',
        'length': '',
        'data': ''
    }

    msg2 = {
        'key': encrypt(str(parser_query_keyid())),
        'id': str(parser_query_uuid()),
        'status': 'seq',
        'address': '',
        'type': 'get_task',
        'length': '',
        'data': ''
    }

    # print("判断是否第一次发包")
    if parser_query_uuid() == '':
        print('第一次发包!!!')
        socketStart(msg1)

    else:
        print('第二次发包, 获取任务!!!')
        socketStart(msg2)

def client_exec_task2():

    '''
    爬虫抓取 12306
    获取任务状态， 反馈结果
    :return:
    '''

    print('爬虫抓取 12306 火车票......')

    pk = NCOREPICKLE()
    count = []

    for i in pk.read_pickle():
        count.append(i)

    def start_qp_ticket():

        aa = Ticketquery()

        for i in pk.read_pickle1():
            # data_convert(aa.query('北京', '包头', '2019-06-20'), 'K55', '软卧 一等卧')
            data_convert(aa.query(i[2], i[3], i[1]), i[0], i[4], i[1])

    if not len(count) == 0:

        t_obj = []  # 定义列表用于存放子线程实例
        for i in range(3):
            t = threading.Thread(target=start_qp_ticket())
            t.start()
            t_obj.append(t)

        for tmp in t_obj:
            tmp.join()  # 为每个子线程添加join之后，主线程就会等这些子线程执行完之后再执行。

        # start_qp_ticket()
        print('关注车票的任务执行成功')

    else:
        print('目前没有关注车票的任务!')

    '''
    try:
        
        pk = NCOREPICKLE()
        # print(pk.read_pickle())

        count = []
        for i in pk.read_pickle():
            print(i)
            count.append(i)

        print(len(count))

        # print(len(pk.read_pickle()))
        def worker():

            aa = Ticketquery()
            data_convert(aa.query('北京', '包头', '2019-06-20'), 'K55', '软卧 一等卧')

        # pool = Pool(10)
        # for i in range(0, len(count)):
        #     pool.apply_async(worker, (i, ))



    except TypeError:
        exit()

    '''

    print('爬虫抓取 12306 火车票 END!!!')

def client_exec_task3():

    print('发送成功结果, to 服务器端 >>> ')

    ok = TASKOK()
    count = []

    for i in ok.read_pickle():
        count.append(i)

    msg = {
        'key': encrypt(str(parser_query_keyid())),
        'id': str(parser_query_uuid()),
        'status': 'seq',
        'address': '',
        'type': 'send_ok',
        'length': '',
        'data': ok.read_pickle()
    }

    if not len(count) == 0:
        socketStart(msg)

    else:
        print('成功列表为空! 暂不向服务端发起请求 ')


def client_schedule(time, job):

    '''
    任务调度
    :param job:
    :return:
    '''

    schedule.every(time).seconds.do(job)

    while True:
        schedule.run_pending()

# def start_job(job):
#     schedule.every(15).seconds.do(job)
#
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

if __name__ == '__main__':

    print('Ncore 分布式客户端节点 [ 正在启动 ..... ]       ')

    # [ 进程1 ]
    p1 = Process(target=client_schedule, args=(15, client_exec_task1))

    # [ 进程2 ]
    # p2 = Process(target=client_schedule, args=(2, client_exec_task2))

    ps2 = []
    for i in range(0, 10):
        p = Process(target=client_schedule, name="p2s"+str(i), args=(2, client_exec_task2))
        ps2.append(p)

    # [ 进程3 ]
    p3 = Process(target=client_schedule, args=(10, client_exec_task3))


    '''
    # pool = Pool(10)
    # for i in range(0, len(count)):
    #     pool.apply_async(worker, (i,))

    # p3 = Process(target=client_schedule, args=(2, client_exec_task2))
    # p4 = Process(target=client_schedule, args=(1, test2))
    # p3.start()
    # p4.start()
    '''


    # 启动进程
    # 进程1
    p1.start()

    # 进程2
    for i in range(0, 10):
        ps2[i].start()

    # 进程3
    p3.start()













    # '''
    # # 压力测试
    #
    # ps = []
    # # 创建子进程实例
    # for i in range(10):
    #     p = Process(target=client_schedule, name="worker" + str(i), args=(1, client_exec_task1))
    #     ps.append(p)
    #
    # # 开启进程
    # for i in range(10):
    #     ps[i].start()
    #
    # '''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socketserver
import struct
import schedule
import time
from multiprocessing import Process
from threading import Thread
import socket

from pycrypto import decrypt
from dbconnect import db_query_keyid, db_write_uuid, TICKETDB
from sendMail import SENDMAIL

uid = '1213'

def unpack(data):

    '''

        拆包功能

        1. 判断初次发包
            验证key号, 返回ID号

        2. 判断返回进度包
        3. 再次获取执行任务

    :param data:
    :return:
    '''

    print('---exec unpack')

    db = eval(data)
    uuid = uid + decrypt(db['key'])

    # 解包 判断初次发包
    print(decrypt(db['key']))
    if db_query_keyid(decrypt(db['key'])) != 0 and db['id'] == '':
        print('初次发包')

        ack_data = {
            'key': decrypt(db['key']),
            'id': str(uuid),
            'status': 'ack',
            'address': '',
            'type': '',
            'username': '',
            'password': '',
            'size': '',
            'data': ''
        }

        print('%s id号, 写入数据库 ' % decrypt(db['key']))
        db_write_uuid(decrypt(db['key']), uuid)

    # 获取执行任务列表
    elif db_query_keyid(decrypt(db['key'])) != 0 and db['type'] == 'get_task' and db['id'] != '':
        print('[ client_exec_task1 ] 获取任务 ')

        ticketdb = TICKETDB()
        ticketdb.delete_lt_now()
        ticket_task = set(ticketdb.select_followticket())

        # 获取任务 mysql db
        ack_data = {
            'key': decrypt(db['key']),
            'id': str(uuid),
            'status': 'an',
            'address': '',
            'type': 'push_task',
            'username': '',
            'password': '',
            'size': '',
            'data': ticket_task
        }

        print(ack_data)

    # 获取成功任务列表
    elif db_query_keyid(decrypt(db['key'])) != 0 and db['type'] == 'send_ok' and db['id'] != '':

        print('[ 获取成功任务列表 ]')
        print(db['data'])

        ticketdb = TICKETDB()

        # 获取用户信息
        print('获取用户信息')
        userinfo = []
        for i in db['data']:
            aa = ticketdb.select_userticket(i[0], i[1], i[4])
            print(aa)

            for k in aa:
                userinfo.append(k)

        print(userinfo)
        print('获取用户信息  --  完毕')


        '''
        注意: 有BUG, 此处数据库userinfo表没有建立与 uid链接
        '''

        # 触发邮件
        smail = SENDMAIL()
        for i in userinfo:
            if not i[0] == '':
                smail.sendmail('2083969687@qq.com', i[1], i[2], i[3])

        # 删除数据库数据
        for i in db['data']:
            ticketdb.delete_followticket(i[0], i[1], i[4])

        print('删除数据库数据成功!!!')

        ack_data = {
            'key': decrypt(db['key']),
            'id': str(uuid),
            'status': 'an',
            'address': '',
            'type': 'delete_task',
            'username': '',
            'password': '',
            'size': '',
            'data': '发送清空task-ok.pk文件指令!!!'
        }

        print(ack_data)

    else:
        print('未识别的数据包!!!')

        ack_data = {
            'key': '',
            'id': '',
            'status': 'Error',
            'address': '',
            'type': '',
            'username': '',
            'password': '',
            'size': '',
            'data': '未识别的数据包!!!'
        }

    return ack_data

def func01():

    '''
            原始方法  -- 串行方式  -- 排队
    :return:
    '''

    sk = socket.socket()
    sk.bind(("0.0.0.0", 9999))
    sk.listen(5)

    while True:

        try:
            conn, address = sk.accept()

            from_server_msglen = conn.recv(4)
            unpack_len_msg = struct.unpack("i", from_server_msglen)[0]

            # 解决粘包
            recv_msg_len = 0
            all_msg = b""
            while recv_msg_len < unpack_len_msg:
                every_recv_date = conn.recv(1024)
                all_msg += every_recv_date                  # 将每次接收到的数据进行拼接和统计
                recv_msg_len += len(every_recv_date)        # 对每次接受到的数据进行累加

            data = all_msg.decode('utf-8')

            # 显示包内容
            print(data)

            # 拆包
            ack = unpack(data)

            # 发送任务指令
            cmd_msg_len = len(ack)
            msg_len_stru = struct.pack('i', cmd_msg_len)

            # 包头大小
            conn.send(msg_len_stru)
            conn.sendall(bytes(str(ack), encoding='utf-8'))

            # self.request.close()
            break

        except Exception:
            pass

ADDRESS = ('0.0.0.0', 9999)
g_socket_server = None
g_conn_pool = []

def func02_init():

    """
        初始化服务端
    """
    global g_socket_server
    g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建 socket 对象
    g_socket_server.bind(ADDRESS)
    g_socket_server.listen(5)  # 最大等待数（有很多人理解为最大连接数，其实是错误的）
    print("服务端已启动，等待客户端连接...")

def func02_accept_client():

    """
        接收新连接
    """
    while True:
        client, _ = g_socket_server.accept()  # 阻塞，等待客户端连接
        # 加入连接池
        g_conn_pool.append(client)
        # 给每个客户端创建一个独立的线程进行管理
        thread = Thread(target=func02_message_handle, args=(client,))
        # 设置成守护线程
        thread.setDaemon(True)
        thread.start()

def func02_message_handle(client):

    """
    消息处理
    """

    while True:

        try:
            # conn, address = sk.accept()
            # self.timeout = 15

            from_server_msglen = client.recv(4)

            if len(from_server_msglen) == 0:
                client.close()
                # 删除连接
                g_conn_pool.remove(client)
                print("有一个客户端下线了。")
                break

            unpack_len_msg = struct.unpack("i", from_server_msglen)[0]

            # 解决粘包
            recv_msg_len = 0
            all_msg = b""
            while recv_msg_len < unpack_len_msg:
                every_recv_date = client.recv(1024)
                all_msg += every_recv_date                  # 将每次接收到的数据进行拼接和统计
                recv_msg_len += len(every_recv_date)        # 对每次接受到的数据进行累加

            data = all_msg.decode('utf-8')

            # 显示包内容
            print(data)

            # 拆包
            ack = unpack(data)

            # 发送任务指令
            cmd_msg_len = len(ack)
            msg_len_stru = struct.pack('i', cmd_msg_len)

            # 包头大小
            client.send(msg_len_stru)
            client.sendall(bytes(str(ack), encoding='utf-8'))

        except Exception:
            pass

def server_exec_process1():

    """
    首次激活, 获得id
    发布任务
    :return:
    """
    func02_init()

    thread = Thread(target=func02_accept_client)
    thread.start()

def server_exec_process2():
    pass

def server_exec_process3():
    pass

def job():
    print('%s [ exec job() 15s test Task .... ] ' % time.ctime())

def server_schedule_seconds(time, job):

    '''
    任务调度
    :param job:
    :return:
    '''

    schedule.every(time).seconds.do(job)

    while True:
        schedule.run_pending()

if __name__ == '__main__':

    HOST, PORT = "0.0.0.0", 9999

    print('Schedule Starting .... ')
    print('Ncoreqp分布式抢票系统监听端口：9999 启动成功')
    print('........')

    # 进程一
    p1 = Process(target=server_exec_process1())
    p1.start()


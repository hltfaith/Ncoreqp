import configparser
import os
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()

def init_parser():
    config["DEFAULT"] = {'uuid': '',
                         'keyid': '',
                         'server': '127.0.0.1',
                         'port': '9999'}

    config["REPTILE"] = {'proxy_type': 'https',
                         'proxy_ip': '203.42.227.113',
                         'proxy_ip_port': '8080'}

    with open(BASE_DIR+'/config/ncorenode.conf', 'w') as configfile:
        config.write(configfile)

def parser_query_uuid():

    '''
    查询uuid结果
    :return:  返回 0 或者 1
    '''

    config.read(BASE_DIR+'/config/ncorenode.conf')
    return config.get("DEFAULT", "uuid")

def parser_query_keyid():

    '''
    查询keyid结果
    :return:
    '''

    config.read(BASE_DIR+'/config/ncorenode.conf')
    return config.get("DEFAULT", "keyid")

def parser_write_uuid(id):

    '''
    写入uuid
    :return:
    '''
    config.read(BASE_DIR+'/config/ncorenode.conf')
    config.set("DEFAULT", "uuid", str(id))
    config.write(open(BASE_DIR+'/config/ncorenode.conf', 'w'))

def parser_query_server():

    '''
    查询server address结果
    :return:
    '''

    config.read(BASE_DIR+'/config/ncorenode.conf')
    return config.get("DEFAULT", "server")

def parser_query_port():

    '''
    查询port结果
    :return:
    '''

    config.read(BASE_DIR + '/config/ncorenode.conf')
    return config.get("DEFAULT", "port")

class NCOREPICKLE(object):

    '''
    持久化存储数据 - 存放接受服务端任务列表
    保存目录 /config/task-data.pk
    :return:
    '''

    def __init__(self):
        self.input = open(BASE_DIR + '/config/task-data.pk', 'rb')

    def write_pickle(self, data):
        output = open(BASE_DIR + '/config/task-data.pk', 'wb')
        pickle.dump(data, output)
        output.close()

    def read_pickle(self):
        data = pickle.load(self.input)
        self.input.close()
        return data

    def read_pickle1(self):
        data = pickle.load(open(BASE_DIR + '/config/task-data.pk', 'rb'))
        self.input.close()
        return data

class TASKOK(object):

    def __init__(self):
        self.input = open(BASE_DIR + '/config/task-ok.pk', 'rb')

    def write_pickle(self, data):
        output = open(BASE_DIR + '/config/task-ok.pk', 'wb')
        pickle.dump(data, output)
        output.close()

    def read_pickle(self):
        data = pickle.load(open(BASE_DIR + '/config/task-ok.pk', 'rb'))
        self.input.close()
        return data


def data_convert(data, lch, type, rq):

    '''
    爬取数据转换车票状态
    :param data: 爬取数据
    :param lch:  列车号
    :param type: 车座类型
    :return:
    '''

    try:

        def conver(value):

            if value == "商务座 特等座":
                num = 4
            elif value == "一等座":
                num = 5
            elif value == "二等座":
                num = 6
            elif value == "高级 软卧":
                num = 7
            elif value == "软卧一等卧":
                num = 8
            elif value == "动卧":
                num = 9
            elif value == "硬卧 二等卧":
                num = 10
            elif value == "软座":
                num = 11
            elif value == "硬座":
                num = 12
            elif value == "无座":
                num = 13
            else:
                print('ERROR: conver')

            return num

        datapk = NCOREPICKLE()
        dataok = TASKOK()

        for i in data:

            if i[0] == lch:

                if i[conver(type)] != '无' and i[conver(type)] != '' and i[conver(type)] != '0':

                    print('%s火车票正在查询, 请稍候.... ' % lch)
                    for k in datapk.read_pickle1():
                        # ('G110', '2019-06-18', '上海', '北京', '商务座 特等座')

                        if lch == k[0] and type == k[4] and rq == k[1]:
                            print('%s列车, 发车时间: %s, %s, 目前有票!!!' % (lch, rq, type))

                            print('读取, dataok.pk文件')
                            count = []
                            for i in dataok.read_pickle():
                                count.append(i)

                            print('有票, 写入pk文件')
                            count_data = []
                            if not len(count) == 0:

                                for i in dataok.read_pickle():

                                    if not i[0] == '':
                                        count_data.append(i)

                                count_data.append(k)
                                dataok.write_pickle(set(count_data))

                            else:
                                data = []
                                data.append(k)
                                dataok.write_pickle(set(data))

                else:
                    print('%s列车, 目前车票没有剩余, 正在拼命重新获取中.....' % lch)

    except TypeError:
        pass

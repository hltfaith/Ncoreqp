#-*- coding:utf8 -*-

import re, sys, os
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from ticket.tool.station import short_name

class Ticketquery(object):
    '''余票查询'''

    def __init__(self):
        self.station_dict = short_name

        self.headers = {
            'Host': 'kyfw.12306.cn',
            'If-Modified-Since': '0',
            'Pragma': 'no-cache',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        self.proxies = {
            'https': '203.42.227.113:8080'
        }

        self.timeout = 15
        self.username = ''
        self.password = ''

    def station_name(self, station):

        '''获取车站简拼'''

        return self.station_dict[station]

    def query(self, from_station, to_station, date):

        '''余票查询'''

        # 出发地 目的地
        fromstation = self.station_name(from_station)
        tostation = self.station_name(to_station)

        # 12306 查询接口
        url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(
            date, fromstation, tostation)

        # 获取余票查询页面
        try:

            html = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=self.timeout, verify=False).json()
            result = html['data']['result']

            querystation = []

            if result == []:
                print('很抱歉,没有查到符合当前条件的列车!')
                exit()

            else:

                for i in result:
                    info = i.split('|')

                    '''
                    info[3]    车次
                    info[4] info[5] 出发站 到达站
                    info[6]  过路站
                    info[8] info[9] 出发时间  到达时间
                    info[10] 历时

                    info[32] 商务座
                    info[31] 一等座
                    info[30] 二等座

                    info[23]  软卧一等卧
                    info[29]  硬座
                    info[28]  硬卧二等卧
                    info[26]  无座

                    info[21]  高级软卧
                    '''

                    cc = info[3]
                    glz = list(self.station_dict.keys())[list(self.station_dict.values()).index(info[6])]
                    ddz = list(self.station_dict.keys())[list(self.station_dict.values()).index(info[5])]
                    cfsj = info[8]
                    ddsj = info[9]
                    lishi = info[10]

                    edz = info[30]
                    ydz = info[31]
                    swz = info[32]

                    rwydz = info[23]
                    ywedz = info[28]
                    yz = info[29]
                    wz = info[26]

                    gjrw = info[21]

                    if re.search('G', cc):

                        '''
                            高铁列车
                            前九段有信息, 后八段没有信息
                        '''
                        querystation.append([cc, str(glz+'-'+ddz), str(cfsj+'-'+ddsj), lishi, swz, ydz, edz, '--', '--', '--', '--',
                                             '--', '--', '--'])

                    elif re.search('D', cc):

                        '''
                            动车列车

                        '''

                        querystation.append([cc, str(glz+'-'+ddz), str(cfsj+'-'+ddsj), lishi, '--', '--', edz, '--', rwydz, '--', ywedz,
                                             '--', '--', wz])

                    elif re.search('T', cc):

                        '''
                            特快列车

                        '''

                        querystation.append([cc, str(glz+'-'+ddz), str(cfsj+'-'+ddsj), lishi, '--', '--', '--', gjrw, ywedz, '--',
                                             ywedz, '--', yz, wz])

                    elif re.search('Z', cc) or re.search('K', cc) or re.search('^\d', cc):

                        '''
                            直达列车 - 快速列车 - 普通列车
                        '''

                        querystation.append([cc, str(glz+'-'+ddz), str(cfsj+'-'+ddsj), lishi, '--', '--', '--', '--', rwydz, '--',
                                             ywedz, '--', yz, wz])

            return querystation

        except requests.exceptions.ProxyError:
            print('Proxy 地址连接超时!!!')

        except requests.exceptions.ConnectTimeout:
            print('连接超时!!!!')

        except requests.exceptions.ReadTimeout:
            print('ReadTimeout!!!')

        except requests.exceptions.ChunkedEncodingError:
            print('EncodingError')

        except:
            print('查询信息有误!请重新输入!')


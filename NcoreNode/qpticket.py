#-*- coding:utf8 -*-

import requests, re, time, ssl
from urllib import parse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import urllib3
import json

'''
12306-余票查询+订票
'''

#不显示警告信息
urllib3.disable_warnings()
ssl._create_default_https_context = ssl._create_unverified_context
req = requests.Session()
req.verify = False
req.cookies['RAIL_DEVICEID'] = 'SZ2FPTOYpAD_crZicAvqbufDoFOyfyvkdmKxR0Objq-2YAKCVYpt_1GdZV-RQL2Ds9pbxvTC5BIjelu7n2LzbN8Z1GNziPGxyBSaJBSZDc_W9tPsdBzl0lSj4UaVvLc9ABnE3vAAM4RkfeEhpR7mIMkzR_L4GuUy'
# req.cookies['RAIL_DEVICEID'] = 'QlT1A55uQG0t4g94cK8py5EJk2IBtohfOmDMkgYupazgyFGy8kYc5SsxiuZnm5hZXvyVwVXPiF-WxPF5STEkfulMlF_fHKF4yf3VDacObJnSN_AKrQYdEdJt1VtzxoRPmA_sgb5KZRUkBI6jqq0l_a9Rhd14bvMJ'

proxies = {
            # 'http': '116.196.90.176:3128',
            'https': '178.143.191.155:8080'
}

timeout = 15

class Login(object):
    '''登录模块'''

    def __init__(self):
        self.url_pic = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.15905700266966694'
        self.url_check = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        self.url_login = 'https://kyfw.12306.cn/passport/web/login'
        self.headers = {
            # 'Host': 'kyfw.12306.cn',
            # 'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        }

        self.proxies = {
            # 'http': '116.196.90.176:3128',
            'https': '203.42.227.113:8080'
        }

        self.timeout = 15

    def showimg(self):
        '''显示验证码图片'''

        try:

            global req
            html_pic = req.get(self.url_pic, headers=self.headers, proxies=self.proxies, timeout=self.timeout, verify=False).content
            open('pic.jpg', 'wb').write(html_pic)
            img = mpimg.imread('pic.jpg')
            plt.imshow(img)
            plt.axis('off')
            plt.show()

        except requests.exceptions.ProxyError:
            print('Proxy 地址连接超时!!!')

        except requests.exceptions.ConnectTimeout:
            print('ConnectTimeout 连接超时!!!!')

        except requests.exceptions.ReadTimeout:
            print('ReadTimeout!!!')

        except requests.exceptions.ChunkedEncodingError:
            print('EncodingError')

        # except:
        #     print('查询信息有误!请重新输入!')

    def captcha(self, answer_num):
        '''填写验证码'''

        answer_sp = answer_num.split(',')
        answer_list = []
        an = {'1': (31, 35), '2': (116, 46), '3': (191, 24), '4': (243, 50), '5': (22, 114), '6': (117, 94),
              '7': (167, 120), '8': (251, 105)}
        for i in answer_sp:
            for j in an.keys():
                if i == j:
                    answer_list.append(an[j][0])
                    answer_list.append(',')
                    answer_list.append(an[j][1])
                    answer_list.append(',')
        s = ''
        for i in answer_list:
            s += str(i)
        answer = s[:-1]

        # 验证验证码
        form_check = {
            'answer': answer,
            'login_site': 'E',
            'rand': 'sjrand',
        }

        try:

            html_check = req.post(self.url_check, data=form_check, headers=self.headers, proxies=self.proxies, timeout=self.timeout, verify=False).json()

            print(html_check)

            if html_check['result_code'] == '4':
                print('验证码校验成功!')
            else:
                print('验证码校验失败!')
                exit()

        except requests.exceptions.ProxyError:
            print('Proxy 地址连接超时!!!')

        except requests.exceptions.ConnectTimeout:
            print('ConnectTimeout 连接超时!!!!')

        except requests.exceptions.ReadTimeout:
            print('ReadTimeout!!!')

        except requests.exceptions.ChunkedEncodingError:
            print('EncodingError')

    def login(self):
        '''登录账号'''

        try:

            data = {
                'username': self.username,
                'password': self.password,
                'appid': 'otn',
            }

            html_login = req.post(self.url_login, data=data, headers=self.headers, proxies=self.proxies, timeout=self.timeout)
            print(html_login.content.decode('utf8'))

            '''
            reponse = json.loads(html_login.content.decode('utf8'))

            if reponse['result_code'] == 0:
                print('恭喜您,登录成功!')

            else:
                print('账号密码错误,登录失败!')
                exit()
            '''

        except json.decoder.JSONDecodeError:
            print('JSONDecodeError 解码失败, 账户登陆失败请联系管理员!!!')

        except requests.exceptions.ProxyError:
            print('Proxy 地址连接超时!!!')

        except requests.exceptions.ConnectTimeout:
            print('ConnectTimeout 连接超时!!!!')

        except requests.exceptions.ReadTimeout:
            print('ReadTimeout!!!')

        except requests.exceptions.ChunkedEncodingError:
            print('EncodingError')

def pass_captcha():

    '''
        自动识别验证码

        自动登录总耗时:  11 秒

    '''

    try:

        print('正在识别验证码...')
        global req
        url_pic = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.15905700266966694'
        url_captcha = 'http://littlebigluo.qicp.net:47720/'

        headers1 = {
            'Referer': 'https://kyfw.12306.cn/otn/login/init',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        }

        html_pic = req.get(url_pic, headers=headers1, proxies=proxies, timeout=15, verify=False).content

        open('pic.jpg', 'wb').write(html_pic)

        files = {
            # 'file': open('pic.jpg', 'rb')
            'pic_xxfile': open('pic.jpg', 'rb')
        }

        headers = {
            'Referer': url_captcha,
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }

        try:

            res = requests.post(url_captcha, files=files, headers=headers, proxies=proxies, timeout=timeout, verify=False).text
            print(res)
            result = re.search('<B>(.*?)</B>', res).group(1).replace(' ', ',')

            return result

        except requests.exceptions.ReadTimeout:
            # print(e)
            pass

    except requests.exceptions.ProxyError:
        print('Proxy 地址连接超时!!!')

    except requests.exceptions.ConnectTimeout:
        print('ConnectTimeout 连接超时!!!!')

    except requests.exceptions.ReadTimeout:
        print('ReadTimeout!!!')

    except requests.exceptions.ChunkedEncodingError:
        print('EncodingError')

    # except:
    #     print('Sorry!验证码自动识别网址已失效~')
    #     exit()

class Order(object):
    '''提交订单'''

    def __init__(self):
        self.url_uam = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        self.url_uamclient = 'https://kyfw.12306.cn/otn/uamauthclient'
        # self.url_order = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        self.url_order = 'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue'
        self.url_token = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        self.url_pass = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        self.url_confirm = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        self.url_checkorder = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        self.url_count = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'

        self.head_1 = {
            'Host': 'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        }

        self.head_2 = {
            'Host': 'kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        }


    def auth(self):

        '''
            验证 uamtk 和 uamauthclient
        '''

        # 验证uamtk
        form = {
            'appid': 'otn',
            # '_json_att':''
        }

        try:

            global req
            html_uam = req.post(self.url_uam, data=form, headers=self.head_1, proxies=proxies, timeout=timeout, verify=False).json()
            print(html_uam)

            if html_uam['result_code'] == 0:
                print('恭喜您,uam验证成功!')
            else:
                print('uam验证失败!')
                exit()

            # 验证uamauthclient
            tk = html_uam['newapptk']

            form = {
                'tk': tk,
                # '_json_att':''
            }

            html_uamclient = req.post(self.url_uamclient, data=form, headers=self.head_1, proxies=proxies, timeout=timeout, verify=False).json()
            print(html_uamclient)

            if html_uamclient['result_code'] == 0:
                print('恭喜您,uamclient验证成功!')
            else:
                print('uamclient验证失败!')
                exit()

        except requests.exceptions.ProxyError:
            print('Proxy 地址连接超时!!!')

        except requests.exceptions.ConnectTimeout:
            print('ConnectTimeout 连接超时!!!!')

        except requests.exceptions.ReadTimeout:
            print('ReadTimeout!!!')

        except requests.exceptions.ChunkedEncodingError:
            print('EncodingError')

    def order(self, result, train_number, from_station, to_station, date):

        '''

            提交订单

        '''

        try:

            global req

            url = "https://kyfw.12306.cn/otn/login/checkUser"

            # result = req.post(url, proxies=proxies, timeout=timeout, verify=False)
            # print(result.text)















            secretStr = result
            # 用户选择要购买的车次的序号
            # secretStr = parse.unquote(result[int(train_number) - 1].split('|')[0])
            back_train_date = time.strftime("%Y-%m-%d", time.localtime())

            form = {
                'secretStr': secretStr,  # 'secretStr':就是余票查询中你选的那班车次的result的那一大串余票信息的|前面的字符串再url解码
                'train_date': date,  # 出发日期(2018-04-08)
                'back_train_date': back_train_date,  # 查询日期
                'tour_flag': 'dc',  # 固定的
                'purpose_codes': 'ADULT',  # 成人票
                'query_from_station_name': from_station,  # 出发地
                'query_to_station_name': to_station,  # 目的地
                'undefined': ''  # 固定的
            }


            newfrom = {


            }

            # html_order = req.post(self.url_order, data=form, headers=self.head_2, proxies=proxies, timeout=timeout, verify=False).json()
            html_order = req.get(self.url_order, data=form, headers=self.head_2, proxies=proxies, verify=False)
            print(html_order)

            # if html_order['status'] == True:
            #     print('恭喜您, 提交订单成功!')
            #
            # else:
            #     print('提交订单失败!')
                # exit()



        except requests.exceptions.ProxyError:
            print('Proxy 地址连接超时!!!')

        except requests.exceptions.ConnectTimeout:
            print('ConnectTimeout 连接超时!!!!')

        except requests.exceptions.ReadTimeout:
            print('ReadTimeout!!!')

        except requests.exceptions.ChunkedEncodingError:
            print('EncodingError')

    def price(self):
        '''打印票价信息'''
        form = {
            '_json_att': ''
        }
        global req
        html_token = req.post(self.url_token, data=form, headers=self.head_1, verify=False).text
        token = re.findall(r"var globalRepeatSubmitToken = '(.*?)';", html_token)[0]
        leftTicket = re.findall(r"'leftTicketStr':'(.*?)',", html_token)[0]
        key_check_isChange = re.findall(r"'key_check_isChange':'(.*?)',", html_token)[0]
        train_no = re.findall(r"'train_no':'(.*?)',", html_token)[0]
        stationTrainCode = re.findall(r"'station_train_code':'(.*?)',", html_token)[0]
        fromStationTelecode = re.findall(r"'from_station_telecode':'(.*?)',", html_token)[0]
        toStationTelecode = re.findall(r"'to_station_telecode':'(.*?)',", html_token)[0]
        date_temp = re.findall(r"'to_station_no':'.*?','train_date':'(.*?)',", html_token)[0]
        timeArray = time.strptime(date_temp, "%Y%m%d")
        timeStamp = int(time.mktime(timeArray))
        time_local = time.localtime(timeStamp)
        train_date_temp = time.strftime("%a %b %d %Y %H:%M:%S", time_local)
        train_date = train_date_temp + ' GMT+0800 (中国标准时间)'
        train_location = re.findall(r"tour_flag':'.*?','train_location':'(.*?)'", html_token)[0]
        purpose_codes = re.findall(r"'purpose_codes':'(.*?)',", html_token)[0]
        print('token值:' + token)
        print('leftTicket值:' + leftTicket)
        print('key_check_isChange值:' + key_check_isChange)
        print('train_no值:' + train_no)
        print('stationTrainCode值:' + stationTrainCode)
        print('fromStationTelecode值:' + fromStationTelecode)
        print('toStationTelecode值:' + toStationTelecode)
        print('train_date值:' + train_date)
        print('train_location值:' + train_location)
        print('purpose_codes值:' + purpose_codes)
        price_list = re.findall(r"'leftDetails':(.*?),'leftTicketStr", html_token)[0]
        # price = price_list[1:-1].replace('\'', '').split(',')
        print('票价:')
        for i in eval(price_list):
            # p = i.encode('latin-1').decode('unicode_escape')
            print(i + ' | ', end='')
        return train_date, train_no, stationTrainCode, fromStationTelecode, toStationTelecode, leftTicket, purpose_codes, train_location, token, key_check_isChange

    def passengers(self, token):
        '''打印乘客信息'''
        # 确认乘客信息
        form = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': token
        }
        global req
        html_pass = req.post(self.url_pass, data=form, headers=self.head_1, verify=False).json()
        passengers = html_pass['data']['normal_passengers']
        print('\n')
        print('乘客信息列表:')
        for i in passengers:
            print(str(int(i['index_id']) + 1) + '号:' + i['passenger_name'] + ' ', end='')
        print('\n')
        return passengers

    def chooseseat(self, passengers, passengers_name, choose_seat, token):
        '''选择乘客和座位'''
        seat_dict = {'无座': '1', '硬座': '1', '硬卧': '3', '软卧': '4', '高级软卧': '6', '动卧': 'F', '二等座': 'O', '一等座': 'M',
                     '商务座': '9'}
        choose_type = seat_dict[choose_seat]
        pass_num = len(passengers_name.split(','))  # 购买的乘客数
        pass_list = passengers_name.split(',')
        pass_dict = []
        for i in pass_list:
            info = passengers[int(i) - 1]
            pass_name = info['passenger_name']  # 名字
            pass_id = info['passenger_id_no']  # 身份证号
            pass_phone = info['mobile_no']  # 手机号码
            pass_type = info['passenger_type']  # 证件类型
            dict = {
                'choose_type': choose_type,
                'pass_name': pass_name,
                'pass_id': pass_id,
                'pass_phone': pass_phone,
                'pass_type': pass_type
            }
            pass_dict.append(dict)

        num = 0
        TicketStr_list = []
        for i in pass_dict:
            if pass_num == 1:
                TicketStr = i['choose_type'] + ',0,1,' + i['pass_name'] + ',' + i['pass_type'] + ',' + i[
                    'pass_id'] + ',' + i['pass_phone'] + ',N'
                TicketStr_list.append(TicketStr)
            elif num == 0:
                TicketStr = i['choose_type'] + ',0,1,' + i['pass_name'] + ',' + i['pass_type'] + ',' + i[
                    'pass_id'] + ',' + i['pass_phone'] + ','
                TicketStr_list.append(TicketStr)
            elif num == pass_num - 1:
                TicketStr = 'N_' + i['choose_type'] + ',0,1,' + i['pass_name'] + ',' + i['pass_type'] + ',' + i[
                    'pass_id'] + ',' + i['pass_phone'] + ',N'
                TicketStr_list.append(TicketStr)
            else:
                TicketStr = 'N_' + i['choose_type'] + ',0,1,' + i['pass_name'] + ',' + i['pass_type'] + ',' + i[
                    'pass_id'] + ',' + i['pass_phone'] + ','
                TicketStr_list.append(TicketStr)
            num += 1

        passengerTicketStr = ''.join(TicketStr_list)
        print(passengerTicketStr)

        num = 0
        passengrStr_list = []
        for i in pass_dict:
            if pass_num == 1:
                passengerStr = i['pass_name'] + ',' + i['pass_type'] + ',' + i['pass_id'] + ',1_'
                passengrStr_list.append(passengerStr)
            elif num == 0:
                passengerStr = i['pass_name'] + ',' + i['pass_type'] + ',' + i['pass_id'] + ','
                passengrStr_list.append(passengerStr)
            elif num == pass_num - 1:
                passengerStr = '1_' + i['pass_name'] + ',' + i['pass_type'] + ',' + i['pass_id'] + ',1_'
                passengrStr_list.append(passengerStr)
            else:
                passengerStr = '1_' + i['pass_name'] + ',' + i['pass_type'] + ',' + i['pass_id'] + ','
                passengrStr_list.append(passengerStr)
            num += 1

        oldpassengerStr = ''.join(passengrStr_list)
        print(oldpassengerStr)
        form = {
            'cancel_flag': '2',
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': passengerTicketStr,
            'oldPassengerStr': oldpassengerStr,
            'tour_flag': 'dc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': token
        }
        global req
        html_checkorder = req.post(self.url_checkorder, data=form, headers=self.head_2, verify=False).json()
        print(html_checkorder)
        if html_checkorder['status'] == True:
            print('检查订单信息成功!')
        else:
            print('检查订单信息失败!')
            exit()

        return passengerTicketStr, oldpassengerStr, choose_type

    def leftticket(self, train_date, train_no, stationTrainCode, choose_type, fromStationTelecode, toStationTelecode,
                   leftTicket, purpose_codes, train_location, token):
        '''查看余票数量'''
        form = {
            'train_date': train_date,
            'train_no': train_no,
            'stationTrainCode': stationTrainCode,
            'seatType': choose_type,
            'fromStationTelecode': fromStationTelecode,
            'toStationTelecode': toStationTelecode,
            'leftTicket': leftTicket,
            'purpose_codes': purpose_codes,
            'train_location': train_location,
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': token
        }
        global req
        html_count = req.post(self.url_count, data=form, headers=self.head_2, verify=False).json()
        print(html_count)
        if html_count['status'] == True:
            print('查看余票数量成功!')
            count = html_count['data']['ticket']
            print('此座位类型还有余票' + count + '张~')
        else:
            print('查看余票数量失败!')
            exit()

    def sure(self):
        '''是否确认购票'''
        # 用户是否继续购票:
        i = input('是否确定购票?(Y or N):')
        if i == 'Y' or i == 'y':
            pass
        else:
            exit()

    def confirm(self, passengerTicketStr, oldpassengerStr, key_check_isChange, leftTicket, purpose_codes,
                train_location, token):
        '''最终确认订单'''
        form = {
            'passengerTicketStr': passengerTicketStr,
            'oldPassengerStr': oldpassengerStr,
            'randCode': '',
            'key_check_isChange': key_check_isChange,
            'choose_seats': '',
            'seatDetailType': '000',
            'leftTicketStr': leftTicket,
            'purpose_codes': purpose_codes,
            'train_location': train_location,
            '_json_att': '',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',
            'REPEAT_SUBMIT_TOKEN': token
        }
        global req
        html_confirm = req.post(self.url_confirm, data=form, headers=self.head_2, verify=False).json()
        print(html_confirm)
        if html_confirm['status'] == True:
            print('确认购票成功!')
        else:
            print('确认购票失败!')
            exit()



# pass_captcha()

''''''

start = time.time()
# 开始订票
login = Login()

# 填写验证码
answer_num = pass_captcha()
login.captcha(answer_num)
login.login()
print('自动登录总耗时: ', int(time.time() - start), '秒')


# 提交订单
# order = Order()
# order.auth()

# 用户选择要购买的车次的序号
# train_number = input('请输入您要购买的车次的序号(例如:6):')
# # 提交订单
# order.order(result, train_number, from_station, to_station, date)

# order.order('tMtA4V0aCtchcay68uoLof0fXMgxsuiibm42i1rU5QZHUBF9tqybweJdZrj1%2B%2B2ZqpqQIpOD0SkV%0AuaeC2fUD0E5u69l%2FfCeQ1i63IbZ9Fy48m6DnFnARUSMbH9B4rrQmEYNhM0z3As733griDw5hw6Vl%0AE23HK9j2OaF0UmClQDmnEmVIO0CCmwZvAkL3R7dIWpNldgrlgEy4jDMNt4P%2F7KQkLQuPE3m4Nzll%0Ah6y%2BrZT7LoEp5QpZ7aNNkYDvCY0teha8nX5eAvz9b87NTDWE0%2FXnCDPvWYGZ4UuuYt87v8IAaJJR%0A', '', '上海', '北京', '2019-04-26')




# 检查订单
# content = order.price()  # 打印出票价信息
# passengers = order.passengers(content[8])  # 打印乘客信息

# # 选择乘客和座位
# passengers_name = input('请选择您要购买的乘客编号(例:1,4):')
# choose_seat = input('请选择您要购买的座位类型(例:商务座):')
# pass_info = order.chooseseat(passengers, passengers_name, choose_seat, content[8])
# # 查看余票数
# order.leftticket(content[0], content[1], content[2], pass_info[2], content[3], content[4], content[5], content[6],
#                  content[7], content[8])
# # 是否确认购票
# order.sure()
# # 最终确认订单
# order.confirm(pass_info[0], pass_info[1], content[9], content[5], content[6], content[7], content[8])










































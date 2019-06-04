# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

from ticket.tool import queryTicket
from ticket.tool import dbconnect

# Create your views here.

# Ncoreqp 注册页面
def regist(request):
    if request.method == 'POST':
        pass

    else:
        pass

# Ncoreqp 登录页面
def login(request):

    '''

        抢票登录页面

    :param request:
    :return:
    '''

    try:
        if request.session.get('is_login', None):
            return redirect('/index/')

    except TypeError:
        pass

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        message = '请检查填写的内容!'
        if username.strip() and password:

            try:

                if(dbconnect.db_login(username, password) != 0):
                    request.session['is_login'] = True
                    request.session['username'] = username

                    return redirect('/index/', locals(), {'username': username})

                else:
                    message = '用户不存在或密码不正确！'
                    return render(request, 'login.html', locals())

            except KeyError:
                return render(request, 'login.html', locals())

        else:
            return render(request, 'login.html', locals())

    return render(request, 'login.html')

# Ncoreqp主页面
def index(request):

    '''

        抢票主页面

        登陆成功

    :param request:
    :return:
    '''

    try:
        is_login = request.session.get('is_login', False)

        if is_login:

            username = request.session['username']

            return render(request, 'ticketIndex.html', {'username': username})
        else:
            return redirect('/login/')

    except TypeError:
        pass

# 退出登录
def logout(request):

    try:

        if not request.session.get('is_login', None):
            # 如果本来就未登录，也就没有登出一说
            return redirect('/login/')

        request.session.flush()

    except TypeError:
        return redirect('/login/')

    return redirect('/login/')

# 预订车票 - 查询列车班次
def cxcp1(request):

    '''抢票过程1页面'''

    return render(request, 'query_order_step1.html', locals())

# 预订车票 - 预订车票
def cxcp2(request):

    '''抢票过程2页面'''

    if request.method == "POST":

        cfcs = request.POST.get('cfcs')
        ddcs = request.POST.get('ddcs')
        cfsj = request.POST.get('cfsj')

        message = '请检查填写的内容!'
        if cfcs.strip() and ddcs.strip() and cfsj.strip():

            try:

                if cfcs != '' and ddcs != '' and cfsj != '':

                    # 出发城市 - 到达城市 - 出发时间 查询
                    ticketinfo = queryTicket.Ticketquery()
                    ticket = ticketinfo.query(cfcs, ddcs, cfsj)

                    count = 1
                    return render(request, 'query_order_step2.html', locals())

                else:
                    message = '内容信息填写不完整！'
                    return render(request, 'query_order_step1.html', locals())

            except KeyError:
                return render(request, 'query_order_step1.html', locals())

        else:
            return render(request, 'query_order_step1.html', locals())

    return render(request, 'query_order_step2.html', locals())

# 预订车票 - 抢票开始
def cxcp3(request):

    '''抢票过程3页面'''

    if request.method == 'GET':

        # 1|6|北京|上海|2019-05-07

        ppid = request.GET.get('ppid')
        username = request.session['username']
        jb = ppid.encode('utf-8')

        if ppid != '':
            cp_info = int(jb.decode().split('|')[0])-1
            cp_local = int(jb.decode().split('|')[1])
            cfcs = str(jb.decode().split('|')[2])
            ddcs = str(jb.decode().split('|')[3])
            cfsj = str(jb.decode().split('|')[4])

            # 出发城市 - 到达城市 - 出发时间 查询
            ticketinfo = queryTicket.Ticketquery()
            ticket = ticketinfo.query(cfcs, ddcs, cfsj)

            # 座位类型
            zw_list = {
                4: '商务座 特等座',
                5: '一等座',
                6: '二等座',
                7: '高级软卧',
                8: '软卧一等卧',
                9: '动卧',
                10: '硬卧 二等卧',
                11: '软座',
                12: '硬座',
                13: '无座',
            }

            try:
                cc_ticket = ticket[cp_info][0]
                cfdd_ticket = ticket[cp_info][1]
                cfddtime_ticket = ticket[cp_info][2]
                ls_ticket = ticket[cp_info][3]
                zwtype_ticket = zw_list[cp_local]

                # 写入进数据库中
                dbconnect.db_write_followticket(str(username), str(cc_ticket), str(cfsj), str(cfddtime_ticket),
                                                str(cfdd_ticket), str(zwtype_ticket), str(cfcs), str(ddcs), str(cfsj))

                # 分布式节点批量扫描

            except TypeError:
                pass

    return render(request, 'query_order_step3.html', locals())

def my_order(request):

    '''我的订单页面'''

    return render(request, 'my_order.html')

def ticket_list(request):

    '''关注车票列表页面'''

    if request.method == 'GET':

        ppid = request.GET.get('ppid')
        username = request.session['username']
        print(username)

        if ppid != '':

            # 获取数据库中的关注车票列表信息
            data = dbconnect.db_select_followticket(username)

            return render(request, 'group_ticket_list.html', locals())


    return render(request, 'group_ticket_list.html')

def setmail(request):

    '''设置邮件发送页面'''

    if request.method == "POST":
        mailaddr = request.POST.get('mailaddr')
        messages = request.POST.get('messages')
        username = request.session['username']

        if mailaddr != '':

            '''
            注意: 此处有BUG, 没有加入check 检查代码!!!
            
            '''

            dbconnect.db_write_mail(str(mailaddr), str(messages), str(username))

        else:
            messageError = '请检查填写的内容!'
            return render(request, 'send_msg.html', locals())

    return render(request, 'send_msg.html', locals())

def listmail(request):

    '''设置邮件发送页面'''

    return render(request, 'buy_msg.html')

def mailIndex(request):

    '''显示邮件列表页面'''

    return render(request, 'mailIndex.html')

def mailIndex2(request):

    '''设置邮件发送页面'''

    return render(request, 'mailIndex2.html')

def airticket_change(request):

    '''退订页面'''

    return render(request, 'airticket_change_regulation.html')



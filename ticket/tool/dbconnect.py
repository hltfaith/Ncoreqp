# -*- coding: utf-8 -*-
import pymysql
import pymysql.cursors

host = '127.0.0.1'
user = 'root'
passwd = '123456'
dbname = 'ticketdb'
charset = 'utf8'

# 连接到数据库
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='123456',
                             db='ticketdb',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

# 查询用户
def db_login(ticket_user, ticket_passwd):

    '''
    验证用户是否在数据库中
    :param ticket_user:
    :param ticket_passwd:
    :return:  返回 0 或者 1
    '''

    db = pymysql.connect(host, user, passwd, dbname)
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM userinfo WHERE ticket_user='%s' AND ticket_passwd='%s';" % (ticket_user, ticket_passwd))

    data = cursor.fetchall()
    db.close()

    return data[0][0]

# 车票列表写入数据库
def db_write_followticket(*args):

    '''
    车票信息写入数据库
    :param args:
    :return:
    '''

    db = pymysql.connect(host, user, passwd, dbname, charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO followticket(ticket_user, ticket_lch, ticket_rq, ticket_sj, ticket_station, ticket_type," \
          " ticket_cjsj, ticket_cfcs, ticket_ddcs, ticket_cfsj) VALUES('%s', '%s','%s', '%s','%s', '%s', DATE(now()), '%s', '%s', '%s');" \
          % (args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7], args[8])
    cursor.execute(sql)
    db.commit()
    db.close()

# 关注车票列表查询
def db_select_followticket(username):

    '''
    车票信息查询
    :param username:
    :return:
    '''

    db = pymysql.connect(host, user, passwd, dbname, charset='utf8')
    cursor = db.cursor()

    cursor.execute("SELECT ticket_lch,ticket_rq,ticket_sj,ticket_station,ticket_type,ticket_cjsj FROM followticket WHERE ticket_user='%s';" % username)

    data = cursor.fetchall()
    # print(data)
    ticket_info_list = []

    num = 1
    for i in data:

        # print(i)
        info_list = []

        for k in i:
            info_list.append(k)

        info_list.insert(0, str(num))
        ticket_info_list.append(info_list)

        num += 1

    db.close()

    return ticket_info_list

# 查询keyid用户
def db_query_keyid(ticket_keyid):

    '''
    验证keyid是否在数据库中
    :param ticket_keyid
    :return:  返回 0 或者 1
    '''

    db = pymysql.connect(host, user, passwd, dbname)
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM keyinfo WHERE ticket_keyid='%s';" % (ticket_keyid))

    data = cursor.fetchall()
    db.close()

    return data[0][0]

# uuid 写入数据库中
def db_write_uuid(ticket_keyid, ticket_uuid):
    db = pymysql.connect(host, user, passwd, dbname, charset='utf8')
    cursor = db.cursor()
    sql = "UPDATE keyinfo SET ticket_uuid='%s' WHERE ticket_keyid='%s';" % (ticket_uuid, ticket_keyid)
    cursor.execute(sql)
    db.commit()
    db.close()


def test(*args):
    db = pymysql.connect(host, user, passwd, dbname, charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO followticket(ticket_user, ticket_lch, ticket_rq, ticket_sj, ticket_station, ticket_type, " \
          "DATA(ticket_cjsj)) VALUES('%s', '%s','%s', '%s','%s', '%s', DATE(now()));" % (
    args[0], args[1], args[2], args[3], args[4], args[5])
    cursor.execute(sql)

    db.commit()
    db.close()

# 插入帐号邮件信息
def db_write_mail(ticket_mail, ticket_message, ticket_user):
    db = pymysql.connect(host, user, passwd, dbname, charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO mailinfo(ticket_mail, ticket_message, ticket_user) VALUES('%s', '%s', '%s');" % (ticket_mail,
    ticket_message, ticket_user)
    cursor.execute(sql)

    db.commit()
    db.close()

class TICKETDB(object):

    def __init__(self):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.db = pymysql.connect(host, user, passwd, dbname, charset='utf8')

    def delete_lt_now(self):

        sql1 = "DELETE from followticket where ticket_cfsj<now() or ticket_rq<now();"
        cursor = self.db.cursor()

        try:
            cursor.execute(sql1)
            self.db.commit()

        except:
            self.db.rollback()

        finally:
            cursor.close()

    def delete_followticket(self, lch, cfsj, type):

        sql1 = "DELETE from followticket where ticket_lch='%s' AND ticket_cfsj='%s' AND ticket_type='%s';" % \
               (lch, cfsj, type)
        cursor = self.db.cursor()

        try:
            cursor.execute(sql1)
            self.db.commit()

        except:
            self.db.rollback()

        finally:
            cursor.close()

    def select_userticket(self, lch, cfsj, type):

        cursor = self.db.cursor()

        try:

            sql = "select ticket_user, ticket_lch, ticket_type, ticket_cfsj from followticket where ticket_lch='%s' and ticket_type='%s' and ticket_cfsj='%s';" % (lch, type, cfsj)
            cursor.execute(sql)
            data = cursor.fetchall()
            return data

        except:
            print('Error: unable to fecth data')

        finally:
            cursor.close()

    def select_followticket(self):

        sql2 = "select ticket_lch, ticket_rq, ticket_cfcs,ticket_ddcs, ticket_type from followticket;"
        cursor = self.db.cursor()
        cursor.execute(sql2)
        data = cursor.fetchall()
        self.db.close()

        return data

    def select_username(self):

        sql2 = "select ticket_lch, ticket_rq, ticket_cfcs,ticket_ddcs, ticket_type from followticket;"
        cursor = self.db.cursor()
        cursor.execute(sql2)
        data = cursor.fetchall()
        self.db.close()

        return data

aa = TICKETDB()


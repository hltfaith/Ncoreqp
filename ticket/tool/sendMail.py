import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

class SENDMAIL(object):

    def __init__(self):
        self.smtpserver = 'smtp.qq.com'
        self.username = 'wu_chang_hao@qq.com'           # 比如QQ邮箱
        self.password = 'xxxxxxxxxxxxxxxx'              # 生成授权码
        self.sender = 'wu_chang_hao@qq.com'

    def sendmail(self, receiver, lch, type, cfsj):

        subject = '【 抢票提醒通知 】'
        receiver = ['%s' % receiver]

        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = 'Ncoreqp-Server <wu_chang_hao@qq.com>'

        msg['To'] = ";".join(receiver)

        # 构造文字内容
        text = """Hi!\n
                  十万火急, 探子来报! \n
                  
                  目前, %s号列车, %s当前有票! - 出发时间为:[ %s ]
                  快去12306网站支付买票吧!!  快速通道链接https://www.12306.cn/index/\n
                  
                  http://www.northcorezh.com\n
                      北芯众合, 改变生活!
                  """ % (lch, type, cfsj)
        text_plain = MIMEText(text, 'plain', 'utf-8')
        msg.attach(text_plain)

        # 发送邮件
        smtp = smtplib.SMTP()
        smtp.connect('smtp.qq.com')

        # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
        # smtp.set_debuglevel(1)
        smtp.login(self.username, self.password)
        smtp.sendmail(self.sender, receiver, msg.as_string())
        smtp.quit()

        print('邮件发送成功 !!!')

    def send_email_by_smtp(self):
        # 用于发送邮件的邮箱。修改成自己的邮箱
        sender_email_address = "wu_chang_hao@qq.com"
        # 用于发送邮件的邮箱的密码。修改成自己的邮箱的密码
        sender_email_password = "xxxxxxxxxxxxxxxxxx"
        # 用于发送邮件的邮箱的smtp服务器，也可以直接是IP地址
        # 修改成自己邮箱的sntp服务器地址；qq邮箱不需要修改此值
        smtp_server_host = "smtp.qq.com"
        # 修改成自己邮箱的sntp服务器监听的端口；qq邮箱不需要修改此值
        smtp_server_port = 465
        # 要发往的邮箱
        receiver_email = "2083969687@qq.com"
        # 要发送的邮件主题
        message_subject = "Python smtp测试邮件"
        # 要发送的邮件内容
        message_context = "这是一封通过Python smtp发送的测试邮件..."

        # 邮件对象，用于构建邮件
        message = MIMEText(message_context, 'plain', 'utf-8')
        # 设置发件人（声称的）
        message["From"] = Header(sender_email_address, "utf-8")
        # 设置收件人（声称的）
        message["To"] = Header(receiver_email, "utf-8")
        # 设置邮件主题
        message["Subject"] = Header(message_subject, "utf-8")

        # 连接smtp服务器。如果没有使用SSL，将SMTP_SSL()改成SMTP()即可其他都不需要做改动
        email_client = smtplib.SMTP_SSL(smtp_server_host, smtp_server_port)
        try:
            # 验证邮箱及密码是否正确
            email_client.login(sender_email_address, sender_email_password)
            print("smtp----login success, now will send an email to {receiver_email}")

        except Exception:
            print("smtp----sorry, username or password not correct or another problem occur")

        else:
            # 发送邮件
            email_client.sendmail(sender_email_address, receiver_email, message.as_string())
            print(f"smtp----send email to {receiver_email} finish")
        finally:
            # 关闭连接
            email_client.close()


from threading import Thread
from flask import current_app
from flask_mail import Message
from datetime import datetime
from models import mail


def send_async_email(app, msg):
    with app.app_context():  # 确认程序上下文被激活
        mail.send(msg)


def send_mail(to, username, authcode, authtype):
    """使用新线程异步发送邮箱
    :param to -> 收件人
    :param username -> 收件人注册时所填写的昵称
    :param authcode -> 生成的邮箱验证码
    :param authtype     -> 注册/找回
    :return 执行线程
    """
    app = current_app._get_current_object()
    if authtype == 0:
        title = '您的账号注册验证码'
        info = '快去完善注册信息吧~'
    elif authtype == 1:
        title = '您的找回密码验证码'
        info = '快去重新设置密码吧~'

    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX'] + title,
                  sender=app.config['FLASK_MAIL_SENDER'],
                  recipients=[to])
    # 邮件内容会以文本和html两种格式呈现，而你能看到哪种格式取决于你的邮件客户端。
    msg.body = 'Sended by flask-email'
    msg.html = '''
    <h1>
        亲爱的 {username},
    </h1>
    <h3>
        欢迎来到 <b>ChatWithAIs</b>!
    </h3>
    <p>
        您的验证码为 &nbsp;&nbsp; <b>{authcode}</b> &nbsp;&nbsp; {info}
    </p>

    <p>感谢您的支持和理解</p>
    <p>来自：HIT ChatWithAIs team</p>
    <p><small>{time}</small></p>
    '''.format(username=username, authcode=authcode, time=datetime.utcnow, info=info)
    thread = Thread(target=send_async_email, args=[app, msg])
    thread.start()
    return thread

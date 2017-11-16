# # coding=utf-8
# from django.core.mail import send_mail
#
# from django.conf import settings
#
# from celery import Celery
#
# import time
#
# # app = Celery('celery_tasks.tasks', broker='redis://172.16.179.130:6379/5')
# app = Celery('celery_task.task', broker='redis://localhost:6379/7')
#
#
# @app.task
# def send_register_active_email(to_email, username, token):
#     subject = '欢迎来到天天生鲜！'
#
#     message = ''
#
#     sender = settings.SECRET_KEY
#
#     receiver = [to_email]
#
#     html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:9090/user/active/%s">http://127.0.0.1:9090/user/active/%s</a>' % (
#
#         username, token, token)
#     send_mail(subject, message, sender, receiver, html_message=html_message)
#
#     time.sleep(5)


# 使用celery
from django.core.mail import send_mail
from django.conf import settings
from celery import Celery
import time

# 初始化django项目所依赖的环境
# import os
# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
# django.setup()

# 创建一个Celery类的对象
app = Celery('celery_tasks.task', broker='redis://127.0.0.1:6379/3')

# 创建任务函数
@app.task
def send_register_active_email(to_email, username, token):
    '''发送激活邮件'''
    subject = '天天生鲜欢迎信息'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:9090/user/active/%s">http://127.0.0.1:9090/user/active/%s</a>' % (
        username, token, token)


    send_mail(subject, message, sender, receiver, html_message=html_message)
    # 模拟邮件发送了5s
    time.sleep(5)

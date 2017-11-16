# coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.views.generic import View

import re

from user.models import User

from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from itsdangerous import SignatureExpired

from  django.conf import settings

from celery_task import task


class Register(View):
    '''
    
        1、首先判断是get还是post请求
        2、get请求定义一个函数，只用来展示页面
        3、psot请求定义一个函数，用来处理接收的参数，还有业务的处理
            注册需要username，pwd，allow，email
            判断是否为空，还有对email的正则判断
            在都不为空的情况下进行业务的处理
    
    '''

    # get请求

    def get(self, request):
        return render(request, 'html/register.html')

    def post(self, request):
        username = request.POST.get('user_name')

        password = request.POST.get('pwd')

        email = request.POST.get('email')

        allow = request.POST.get('allow')

        # 判断是否填入内容

        if not all([username, password, email]):
            return render(request, 'html/register.html', {'errmsg': '数据不完整'})

        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'html/register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'html/register.html', {'errmsg': '请勾选协议！'})

        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            user = None

        if user:
            return render(request, 'html/register.html', {'errmsg': '用户已经存在！'})

        user = User.objects.create_user(username, email, password)

        user.is_active = 0

        user.save()

        serializer = Serializer(settings.SECRET_KEY, 3600)

        info = {'confirm': user.id}

        token = serializer.dumps(info)

        token = token.decode()

        task.send_register_active_email(email, username, token)

        return redirect(reverse('goods:index'))


class ActicateView(View):
    def get(self, request, token):

        serializer = Serializer(settings.SECRET_KEY, 3600)

        try:
            info = serializer.loads(token)

            user_id = info['confirm']

            user = User.objects.get(id=user_id)

            user.is_active = 1

            user.save()

            return redirect(reverse('user:login'))

        except SignatureExpired as e:

            return HttpResponse('活动链接已经失效，请重新注册！！！')


class LoginView(View):
    def get(self, request):

        if 'username' in request.COOKIES:

            username = request.COOKIES.get('username')

            checked = 'checked'

        else:

            username = ''
            checked = ''

        return render(request, 'html/login.html', {'username': username, 'checked': checked})

    def post(self, request):

        username = request.POST.get('username')

        password = request.POST.get('pwd')

        if not all([username, password]):
            return render(request, 'html/login.html', {'errmsg': '数据不完整'})

        user = authenticate(username=username,password=password)


        if user is not None:

            if user.is_active:

                login(request, user)

                response = redirect(reverse('goods:index'))

                remember = request.POST.get('remember')

                if remember == 'on':
                    response.set_cookie('username', username)

                else:
                    response.delete_cookie('username')

                return response


            else:
                return render(request, 'html/login.html', {'errmsg': '账户没有激活'})

        else:

            return render(request, 'html/login.html', {'errmsg': '用户名或者密码错误'})

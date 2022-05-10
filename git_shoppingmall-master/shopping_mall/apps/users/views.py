from django.shortcuts import render
import json
import re
from django.contrib.auth import login
from django.utils import http
from django_redis import get_redis_connection
from apps.users.models import User

# Create your views here.
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import logout

from django.contrib.auth.mixins import LoginRequiredMixin
from utils.views import LoginRequiredJSONMixin


class RegisterView(View):
    def post(self, request):
        json_dict = json.loads(request.body)

        username = json_dict.get('username')
        password = json_dict.get('password')
        password2 = json_dict.get('password2')
        mobile = json_dict.get('mobile')
        sms_code = json_dict.get('sms_code')
        allow = json_dict.get('allow')

        if not all(['username', 'password', 'password2', 'mobile', 'sms_code', 'allow']):
            return JsonResponse({'code': 400, 'errmsg': '数据不全'})
        if not re.match(r'^[a-zA-Z0-9_]{5,20}$', username):
            return JsonResponse({'code': 400, 'errmsg': 'username格式有误!'})
        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': 'password格式有误!'})
        # 判断两次密码是否一致
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次输入不对!'})
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': 'mobile格式有误!'})
        # 判断是否勾选用户协议
        if allow != True:
            return JsonResponse({'code': 400, 'errmsg': 'allow格式有误!'})

        user = User.objects.create_user(username=username, password=password, mobile=mobile)
        login(request, user)

        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()

        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


class LoginView(View):
    def post(self, request):
        data = json.loads(request.body.decode())

        username = data.get('username')
        password = data.get('password')
        remembered = data.get('remember')
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})

        # 多用户登陆，通过正则判断用户输入的是电话号码还是用户名，然后返回username再进行判别
        if re.match('1[3-9]\d{9}', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'

        from django.contrib.auth import authenticate

        user = authenticate(username=username, password=password)

        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})
        from django.contrib.auth import login
        login(request, user)

        if remembered:
            request.session.set_expiry(None)

        else:
            request.session.set_expiry(0)

        response = JsonResponse({'code': 0, 'errmsg': 'ok'})

        response.set_cookie('username', username)
        # response.set_cookie('username',username)
        #
        # from apps.carts.utils import merge_cookie_to_redis

        # response =
        return response


class LogoutView(View):
    def delete(self, request):
        logout(request)

        response = JsonResponse({'code': 0,
                                 'errmsg': 'ok'})

        response.delete_cookie('username')

        return response


#
# class UserInfoView(LoginRequiredMixin, View):
#     def get(self, request):
#         info_data = {
#             'username': request.user.username,
#             'email': request.user.email,
#             'mobile': request.user.mobile,
#             'email_active': request.user.email_active,
#         }
#
#         return JsonResponse({'code': 0, 'errmsg': 'ok', 'info_data': info_data})
class CenterView(LoginRequiredJSONMixin, View):
    def get(self, request):
        # request.user 就是 已经登录的用户信息
        # request.user 是来源于 中间件
        # 系统会进行判断 如果我们确实是登录用户，则可以获取到 登录用户对应的 模型实例数据
        # 如果我们确实不是登录用户，则request.user = AnonymousUser()  匿名用户
        info_data = {
            'username': request.user.username,
            'email': request.user.email,
            'mobile': request.user.mobile,
            'email_active': request.user.email_active,
        }

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'info_data': info_data})


class EmailView(LoginRequiredJSONMixin, View):
    def put(self, request):
        data = json.loads(request.body.decode())

        email = data.get('email')

        user = request.user
        user.email = email
        user.save()

        from django.core.mail import send_mail

        subject = '邮件激活'

        from apps.users.utils import generic_email_verify_token
        token = generic_email_verify_token(request.user.id)

        verify_url = "http://www.meiduo.site:8080/success_verify_email.html?token=%s" % token

        # 发送的信息

        message = ''

        html_message = '<p>尊敬的用户您好！</p>' \
                       '<p>感谢您使用美多商城。</p>' \
                       '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                       '<p><a href="%s">%s<a></p>' % (email, verify_url, verify_url)

        # 发送人
        from_email = 'k_lay0@163.com'

        # 收信人
        recipient_list = ['1018519785@qq.com,k_lay0@163.com']

        from celery_tasks.send_email.tasks import celery_send_emails
        # send_emails(subject=subject,
        #           message=message,
        #           from_email=from_email,
        #           recipient_list=recipient_list)
        celery_send_emails.delay(subject=subject,
                                 message=message,
                                 from_email=from_email,
                                 recipient_list=recipient_list,
                                 html_message=html_message)

        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class EmailVerifyView(View):
    def put(self, request):
        params = request.GET
        token = params.get('token')
        if token is None:
            return JsonResponse({'code': 400, 'errmsg': '参数缺失'})

        from apps.users.utils import check_verify_token
        user_id = check_verify_token(token)

        if user_id is None:
            return JsonResponse({'code': 400, 'errmsg': '参数错误'})

        user = User.objects.get(id=user_id)

        user.email_active = True
        user.save()

        return JsonResponse({'code': 0, 'errmsg': 'ok'})

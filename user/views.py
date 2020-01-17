import base64
import hashlib
import json
import random

import redis
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from cutepet.settings import TESTURL
from dtoken.views import make_token
from user.models import User
from .task import send_active_email


def testview(request):
    data = json.loads(request.body)
    print(data)
    return JsonResponse({'code': 200})


class Users(View):
    def post(self, request):
        if request.method != 'POST':
            return JsonResponse({'code': 10100, 'error': 'PLease use POST'})
        data = json.loads(request.body)

        username = data.get('username')
        password = data.get('password')
        password_1 = data.get('password_1')
        email = data.get('email')
        phone = data.get('phone')

        # 校验数据
        if password != password_1:
            return JsonResponse({'code': 10101, 'error': 'Please confirm your password'})
        old_user = User.objects.filter(username=username)
        if old_user:
            return JsonResponse({'code': 10102, 'error': 'Sorry! Your nickname has already used'})

        # 密码转化
        m = hashlib.md5()
        m.update(password.encode())
        pwd = m.hexdigest()

        try:
            user = User.objects.create(username=username, password=pwd, email=email, phone=phone)
        except:
            return JsonResponse({'code': 10102, 'error': 'Please submit data in correct style'})

        # 生成,签发token
        token = make_token(username)

        # 发送激活邮件
        random_int = random.randint(1000, 9999)
        code_str = username + str(random_int)
        code_str_bs = base64.urlsafe_b64encode(code_str.encode())

        # 将随机码储存在redis中,过期时间两天
        # TODO 上线后增加密码  为什么存redis
        r = redis.Redis(host='127.0.0.1', port='6379', db=1)
        r.set('email_active_%s' % username, code_str_bs, ex=3600 * 12 * 2)
        # TODO 上线后修改地址
        active_url = TESTURL + '/cutepet/templates/active.html?code=%s' % code_str_bs.decode()

        #异步发邮件
        send_active_email.delay(email, active_url)
        result = {'code': 200, 'username': username, 'data': {'token': token.decode()}}
        return JsonResponse(result)


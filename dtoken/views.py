import hashlib
import json
import time

import jwt
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from cutepet.settings import JWT_TOKEN_KEY
from user.models import User


def tokenview(request):
    if request.method != 'POST':
        return JsonResponse({'code':10001,'error':'Please use post method'})
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    user = User.objects.filter(username=username)
    if not user:
        return JsonResponse({'code':10003,'error':'Please give right username and password'})

    user = user[0]
    m = hashlib.md5()
    m.update(password.encode())
    if m.hexdigest() != user.password:
        print('result')
        return JsonResponse({'code':10003,'error':'please give me right username and password'})

    # 用户名密码正确,签发token
    token = make_token(username)
    result = {'code':200,'username':username,'data':{'token':token.decode()}}
    print(result)
    print('*'*50)
    return JsonResponse(result)

def make_token(username,exp=3600*24):
    key = JWT_TOKEN_KEY
    now = time.time()
    payload = {'username':username,'exp':exp+now}
    return jwt.encode(payload,key,algorithm='HS256')

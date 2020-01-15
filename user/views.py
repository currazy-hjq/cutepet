import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
def testview(request):
    data = json.loads(request.body)
    print(data)
    return JsonResponse({'code':200})

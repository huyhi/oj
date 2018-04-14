#coding=utf-8
import hashlib
import json
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from . import models
import logging
logger = logging.getLogger('request')
from django.conf import settings

def index(request):
    """
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    """
    if request.method == "GET":
        if request.GET :
            signature = request.GET.get("signature", None)
            timestamp = request.GET.get("timestamp", None)
            nonce = request.GET.get("nonce", None)
            echostr = request.GET.get("echostr", None)
            token = settings.SECRET_KEY

            list = [token, timestamp, nonce]
            list.sort()
            tmp_str = "%s%s%s" % tuple(list)
            hashcode = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()

            if hashcode == signature:
                return HttpResponse(echostr)
            else:
                return HttpResponse("")
        else:
            return HttpResponse("hello, this is handle view")

#def index(request):
#    return HttpResponse('Hello,world!')


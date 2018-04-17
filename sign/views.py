from django.shortcuts import render
from django.http import JsonResponse
from sign.models import Event
import datetime
from django.views.decorators.csrf import csrf_exempt

def teacher_index(request):
    return render(request, "sign_teacher_index.html")

def student_index(request):
    return render(request, "sign_student_index.html")

@csrf_exempt
def startSign(request):

    user = request.user

    if request.method == 'POST' and user.is_admin:   #judge HTTP method and user identity
        
        #start a new sign event
        
        Event.objects.create(
            position = request.POST.get('position'),    #点名发起的位置，以此来判断学生是否在指定范围内签到
            has_signed_count = 1,
            all_student_count = 1,
            started_time = request.POST.get('started_time', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),    #点名开始的时间，可自定义
            banji_id = 1,
            teacher_id = user.id
        )

        return JsonResponse({
            'success': True,
            'errMsg': None,
            'position': request.POST.get('position')
        })

    else:

        return JsonResponse({
            'success': False,
            'errMsg': 'Permission denied'
        })
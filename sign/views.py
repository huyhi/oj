from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from sign.models import Event
from work.models import BanJi
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta


#恕我直言，php7 web 后端不是秒杀 python3 ?
def teacher_index(request):

    user = request.user

    if request.method == 'GET' and user.is_admin:    
        page = request.GET.get('page', 1)

        signList = Event.objects.all().filter(teacher_id = 1).prefetch_related('banji').values(
            'position', 'has_signed_count', 'all_student_count', 'created_time', 'started_time', 'banji__name'
        )

        perPage = Paginator(signList, 10)     # @10 items per page, use query params page
        try:
            data = perPage.page(page)   
        except EmptyPage:
            data = perPage.page(perPage.num_pages)

        return render(request, "sign_teacher_index.html", {
            'data': data
        })


"""
教师创建点名的路由 Http Method POST
必要参数：banji_id，position详细信息
可选参数：started_time，预约点名开始的时间，如不填则默认现在

TODO
！安全隐患！
由于测试方便，这里暂时禁用了CSRF，后续需要启用CSRF防御机制
"""
@csrf_exempt
def create(request):

    user = request.user

    if request.method == 'POST' and user.is_admin:   #judge HTTP method and user identity

        banjiId = request.POST.get('banji_id')
        timeNow = datetime.now()

        Event.objects.create(
            position = request.POST.get('position'),    #点名发起的位置，以此来判断学生是否在指定范围内签到
            has_signed_count = 0,
            #all_student_count = BanJi.objects.filter(BanJi__contains='Lennon').count()
            #all_student_count = BanJi.objects.filter(id = banjiId).annotate(count = Count('banJi_students')).values('count'),
            all_student_count = 1,      #需要根据 banjiId 来获得应该签到的总人数，还不是太熟悉 Django Query Set Api，暂时写死为 1
            started_time = request.POST.get('started_time', timeNow.strftime('%Y-%m-%d %H:%M:%S')),     #点名开始的时间，可自定义
            closed_time = request.POST.get('closed_time', (timeNow + timedelta(minutes = 10)).strftime('%Y-%m-%d %H:%M:%S')),    #点名结束的时间，默认10min的点名期限
            banji_id = banjiId,
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



def student_index(request):
    return render(request, "sign_student_index.html")
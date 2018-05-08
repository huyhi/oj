from django.http import JsonResponse, HttpResponse
from django.db import connection
from django.db.models import Count
from sign.models import Event, Sign
from work.models import BanJi
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta


def teacher_index(request):

    user = request.user

    if request.method == 'GET' and user.is_admin:    
        page = int(request.GET.get('page', 1))

        signList = Event.objects.all().filter(teacher_id = user.id).prefetch_related('banji').values(
            'position', 'has_signed_count', 'all_student_count', 'created_time', 'started_time', 'closed_time', 'banji__name'
        )

        # @10 items per page, use query params page
        perPage = Paginator(signList, 10)     
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
需要增加用户验证的中间件。。。。具体怎么在Django实现我还在查看文档。。。。
由于测试方便，这里暂时禁用了CSRF，后续需要启用CSRF防御机制
"""

@csrf_exempt
def create(request):

    user = request.user

    if request.method == 'POST' and user.is_admin:   #judge HTTP method and user identity

        banjiId = int(request.POST.get('banji_id'))
        timeNow = datetime.now()

        Event.objects.create(
            position = request.POST.get('position'),    #点名发起的位置，以此来判断学生是否在指定范围内签到
            has_signed_count = 0,
            all_student_count = BanJi.objects.get(id = banjiId).students.count(),
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
        

def detail(request, eventId):

    page = int(request.GET.get('page', 1))

    studentsList = Sign.objects.filter(event = eventId).prefetch_related('user').values(
        'user__username', 'created_time'
    )

    # @10 items per page, use query params page
    perPage = Paginator(studentsList, 10)     
    try:
        data = perPage.page(page)   
    except EmptyPage:
        data = perPage.page(perPage.num_pages)

    return render(request, "sign_detail.html", {
        'data': data
    })



#感觉 Django 的 orm 模型很别扭，不习惯
@csrf_exempt
def student_index(request):

    userId = request.user.id
    data = {}
    cursor = connection.cursor()

    ongoingSQL = '\
        select e.* \
        from sign_event AS e\
        join \
        (\
            select bj_mid.banji_id \
            from work_banji_students AS bj_mid\
            join work_banji AS bj\
            on bj_mid.banji_id = bj.id and bj_mid.myuser_id = %d\
            where now() between bj.start_time and bj.end_time\
        ) AS tmp\
        on e.banji_id = tmp.banji_id\
        where now() between e.started_time and e.closed_time\
    ' % userId

    cursor.execute(ongoingSQL)
    data['onGoing'] = cursor.fetchall()

    checkedSQL = ''

    return JsonResponse(data)
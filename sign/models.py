"""
modified at 2018/4/15

include two scheme

sign_event
签到事件表，由教师用户发起

sign_sing
学生签到表

"""

from django.db import models
from auth_system.models import MyUser
from work.models import BanJi

class Event(models.Model):
    teacher = models.ForeignKey(MyUser, related_name = 'teacher', on_delete = models.CASCADE)
    banji = models.ForeignKey(BanJi, related_name = 'banji', on_delete = models.CASCADE)
    position = models.CharField(max_length = 1024)
    has_signed_count = models.IntegerField()
    all_student_count = models.IntegerField()
    created_time = models.DateTimeField(auto_now = True)
    started_time = models.DateTimeField()
    closed_time = models.DateTimeField()


class Sign(models.Model):
    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete = models.CASCADE)
    created_time = models.DateTimeField(auto_now = True)
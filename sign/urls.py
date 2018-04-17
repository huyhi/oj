from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^sign/teacher_sign$', views.teacher_index, name='sign.teacher.index'),
    url(r'^sign/student_sign$', views.student_index, name='sign.student.index'),
    url(r'^start_sign_prj$', views.startSign, name='sign.start')
]
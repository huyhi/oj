from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^teacher_sign$', views.teacher_index, name='sign.teacher.index'),
    url(r'^create$', views.create, name='sign.create'),
    url(r'^detail/(\d+)$', views.detail, name='sign.detail'),

    url(r'^student_sign$', views.student_index, name='sign.student.index'),
    # url(r'^sign/(\d+)$', views.sign, name='sign.sign')
]
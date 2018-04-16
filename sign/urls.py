from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='sign.index'),
    url(r'^start_sign_prj$', views.startSign, name='sign.start')
]
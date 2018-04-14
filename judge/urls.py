from django.conf.urls import url, include
from .views import  select_point, delete_problem, add_problem, ProblemDetailView, update_problem, \
    add_choice,list_problems,list_choices,del_choice_problem,ChoiceProblemDetailView,update_choice_problem, verify_file,list_tiankong,list_gaicuo,add_tiankong,update_tiankong,TiankongProblemDetailView,delete_tiankong,add_gaicuo,update_gaicuo,GaicuoProblemDetailView,delete_gaicuo

urlpatterns = [
    url(r'pointslect', select_point, name='select_point'),
    url(r'verify-file',verify_file,name='verify_file'),

    url(r'^choice_problem_list/',list_choices,name='choice_problem_list'),
    url(r'add-choice', add_choice, name='add_choice_problem'),
    url(r'^del-choice-problem',del_choice_problem,name='del_choice_problem'),
    url(r'update-choice-$',update_choice_problem,name='_update_choice_problem'),
    url(r'update-choice-(?P<id>\d+)/$',update_choice_problem,name='update_choice_problem'),
    url(r'^choice-detail-$',ChoiceProblemDetailView.as_view(),name='_choice_problem_detail'),
    url(r'^choice-detail-(?P<pk>\d+)/$',ChoiceProblemDetailView.as_view(),name='choice_problem_detail'),

    url(r'^problem_list/$', list_problems, name='problem_list'),
    url(r'add-problem', add_problem, name='add_problem'),
    url(r'^del-problem/$', delete_problem, name='del_problem'),
    url(r'^update-biancheng-$', update_problem, name='_update_problem'),
    url(r'^update-biancheng-(?P<id>\d+)/$', update_problem, name='update_problem'),
    url(r'^problem-detail-$', ProblemDetailView.as_view(), name='_problem_detail'),
    url(r'^problem-detail-(?P<pk>\d+)/$', ProblemDetailView.as_view(), name='problem_detail'),

    url(r'tiankong_problem_list',list_tiankong,name='tiankong_problem_list'),
    url(r'add_tiankong',add_tiankong,name='add_tiankong'),
    url(r'^del-tiankong',delete_tiankong,name='del_tiankong'),
    url(r'update-tiankong-$',update_tiankong,name='_update_tiankong'),
    url(r'update-tiankong-(?P<id>\d+)/$',update_tiankong,name='update_tiankong'),
    url(r'^tiankong-detail-$',TiankongProblemDetailView.as_view(), name='_tiankong_detail'),
    url(r'^tiankong-detail-(?P<pk>\d+)/$',TiankongProblemDetailView.as_view(), name='tiankong_problem_detail'),

    url(r'gaicuo_problem_list',list_gaicuo,name='gaicuo_problem_list'),
    url(r'add_gaicuo',add_gaicuo,name='add_gaicuo'),
    url(r'^del-gaicuo',delete_gaicuo,name='del_gaicuo'),
    url(r'update-gaicuo-$',update_gaicuo,name='_update_gaicuo'),
    url(r'update-gaicuo-(?P<id>\d+)/$',update_gaicuo,name='update_gaicuo'),
    url(r'^gaicuo-detail-$',GaicuoProblemDetailView.as_view(), name='_gaicuo_detail'),
    url(r'^gaicuo-detail-(?P<pk>\d+)/$',GaicuoProblemDetailView.as_view(), name='gaicuo_problem_detail'),
]


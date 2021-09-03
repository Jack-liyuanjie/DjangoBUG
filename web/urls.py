from django.urls import path
from django.conf.urls import url, include
from web.views import account, home, project, statistics, wiki, file, setting, issues, dashboard

app_name = 'web'

urlpatterns = [
    path('register', account.register, name='register'),  # register
    path('send_sms', account.send_sms, name='send_sms'),  # send_sms
    path('login_sms', account.login_sms, name='login_sms'),  # login_sms
    path('image_code', account.image_code, name='image_code'),
    path('login', account.login, name='login'),
    path('logout', account.logout, name='logout'),
    path('index', home.index, name='index'),

    path('price', home.price, name='price'),
    url(r'^payment/(?P<policy_id>\d+)/$', home.payment, name='payment'),
    url(r'^pay/$', home.pay, name='pay'),
    url(r'^pay/notify/$', home.pay_notify, name='pay_notify'),

    # 项目列表
    path('project/list', project.project_list, name='project_list'),

    # /project/star/my/1
    # /project/star/join/1
    url(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_star, name='project_star'),
    url(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_unstar, name='project_unstar'),

    # 项目管理
    url(r'manage/(?P<project_id>\d+)/', include([
        url(r'^dashboard/$', dashboard.dashboard, name='dashboard'),
        url(r'^dashboard/issues/chart/$', dashboard.issues_chart, name='issues_chart'),

        url(r'^issues/$', issues.issues, name='issues'),
        url(r'^issues/detail/(?P<issues_id>\d+)/$', issues.issues_detail, name='issues_detail'),
        url(r'^issues/record/(?P<issues_id>\d+)/$', issues.issues_record, name='issues_record'),
        url(r'^issues/change/(?P<issues_id>\d+)/$', issues.issues_change, name='issues_change'),
        url(r'^issues/invite/url/$', issues.invite_url, name='invite_url'),

        url(r'^statistics/$', statistics.statistics, name='statistics'),
        url(r'^statistics/priority$', statistics.statistics_priority, name='statistics_priority'),
        url(r'^statistics/statistics_project/user', statistics.statistics_project_user, name='statistics_project_user'),

        url(r'^wiki/$', wiki.wiki, name='wiki'),
        url(r'^wiki/add$', wiki.wiki_add, name='wiki_add'),
        url(r'^wiki/catalog$', wiki.wiki_catalog, name='wiki_catalog'),
        url(r'^wiki/delete/(?P<wiki_id>\d+)/$', wiki.wiki_delete, name='wiki_delete'),
        url(r'^wiki/edit/(?P<wiki_id>\d+)/$', wiki.wiki_edit, name='wiki_edit'),
        url(r'^wiki/upload', wiki.wiki_upload, name='wiki_upload'),

        url(r'^file/$', file.file, name='file'),
        url(r'^file/delete/$', file.file_delete, name='file_delete'),
        url(r'cos/cos_credential/$', file.cos_credential, name='cos_credential'),
        url(r'file/post/$', file.file_post, name='file_post'),
        url(r'file/download/(?P<file_id>\d+)/$', file.file_download, name='file_download'),

        url(r'^setting/$', setting.setting, name='setting'),
        url(r'^setting/delete/$', setting.delete, name='setting_delete'),

    ], None)),
    url(r'^invite/join/(?P<code>\w+)/$', issues.invite_join, name='invite_join'),
]
# 项目管理
# url(r'^manage/(?P<project_id>\d+)/dashboard/$', project.project_list, name='project_star'),
# url(r'^manage/(?P<project_id>\d+)/issues/$', project.project_list, name='project_star'),
# url(r'^manage/(?P<project_id>\d+)/statistics/$', project.project_list, name='project_star'),
# url(r'^manage/(?P<project_id>\d+)/file/$', project.project_list, name='project_star'),
# url(r'^manage/(?P<project_id>\d+)/wiki/$', project.project_list, name='project_star'),
# url(r'^manage/(?P<project_id>\d+)/setting/$', project.project_list, name='project_star'),

from django.urls import path
from . import views

app_name ='system'

urlpatterns = [
    path('main.html', views.main),
    path('btnAction', views.btn_action),
    path('getdiskStatus', views.get_diskstatus),
    path('sysconfig.html', views.system_config),
    path('usrconfig.html', views.usr_config),
    path('newusr.html', views.new_usr),
    path('heartbeat',views.heartbeat),
    path('searchmid.html',views.search_mid),
    path('audiofile.html', views.audio_file),
    path('free_log', views.free_logs),
    path('free.html',views.free_count),
    path('delete.html',views.del_usr),
    path('recordStatus',views.record_status),
    path('devices',views.devices),
    path('netconfig.html',views.net_config),
    path('remotectr.html',views.remote_control),
    path('channelconfig.html',views.channel_config),
    path('getval',views.get_val)

]
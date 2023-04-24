from django.urls import path
from . import views

app_name ='system'

urlpatterns = [
    path('main.html', views.main),
    path('getdiskStatus', views.get_diskStatus),
    path('isRecordStatusOk',views.get_isRecordStatusOk),#新增
    path('sysconfig.html', views.system_config),
    path('usrconfig.html', views.usr_config),
    path('newusr.html', views.new_usr),
    path('sendData',views.send_data),
    path('heartbeat',views.get_heartbeat),
    path('getAudioState',views.get_audiostatus), #获取音频状态
    path('searchmid.html',views.search_mid),
    path('audiofile.html', views.audio_file),
    path('free_log', views.free_logs),
    # path('free.html',views.free_html),
    path('free.html',views.free_count),
    path('delete.html',views.del_usr),
    path('recordStatus',views.record_status),
    path('devices',views.devices),
    path('netconfig.html',views.net_config),
    path('remotectr.html',views.remote_control),
    path('edit.html',views.edit_usr),#新增
]
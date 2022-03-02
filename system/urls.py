from django.urls import path
from . import views

app_name ='system'

urlpatterns = [
    path('main.html', views.main),
    path('getdiskStatus', views.get_diskstatus),
    path('sysconfig.html', views.system_config),
    path('usrconfig.html', views.usr_config)


]
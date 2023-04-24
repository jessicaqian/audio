from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import NameForm
from . import forms
# import sqlite3
import configparser
import time,datetime,os
import hashlib

# Create your views here.

now = datetime.datetime.now()

timestr = now.strftime("%Y-%m-%d")
dir = os.getcwd() + '/logs'
if not os.path.exists(dir):
    os.mkdir(dir)
file_path = dir + '/' + timestr + '.txt'


def login(request):
    if request.session.get('is_login',None):
        return redirect('/system/main.html/')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            info = form.cleaned_data # 就是读取表单返回的值
            timenow = datetime.datetime.now()
            T_Now = timenow.minute + timenow.hour * 60
            usrname = info['usrname'] #表单中的姓名

            config = configparser.ConfigParser()
            config.read("web.ini")
            config.set(usrname, "is_login", 'true')
            config.set(usrname, "t_current", str(T_Now))

            usrpermiss = config.get('usrinfo', usrname)
            config.write(open("web.ini", "w"))

            now = datetime.datetime.now()
            now_time = now.strftime("%Y-%m-%d %H:%M:%S")

            with open(file=file_path, mode="a", encoding="utf-8") as f:
                f.write(f'{now_time} 用户: {usrname} 登录\n')
            print(usrpermiss)
            return HttpResponseRedirect('/system/main.html?name='+usrname+'&permiss='+usrpermiss)
        else:
            return render(request, 'admin/login.html', {'form': form})
    else:
        form = NameForm()
    return render(request, 'admin/login.html', {'form': form})


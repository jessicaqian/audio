from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import NameForm
from . import forms
# import sqlite3
import configparser
import time,datetime,os

# Create your views here.

now = datetime.datetime.now()

timestr = now.strftime("%Y-%m-%d")
dir = os.getcwd() + '/logs'
if not os.path.exists(dir):
    os.mkdir(dir)
file_path = dir + '/' + timestr + '.txt'


def login(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            info = form.cleaned_data
            timenow = datetime.datetime.now()
            T_Now = timenow.minute + timenow.hour * 60
            usrname = info['usrname']

            config = configparser.ConfigParser()
            config.read("web.ini")
            config.set(usrname, "is_login", 'true')
            config.set(usrname, "t_current", str(T_Now))

            usrpermiss = config.get('usrinfo', usrname)
            config.write(open("web.ini", "w"))

            # conn = sqlite3.connect('db.sqlite3')
            # cursor = conn.cursor()
            # sql = " SELECT usrpermiss FROM usradmin WHERE usrname='" + usrname + "'"
            # cursor.execute(sql)
            # val = cursor.fetchone()
            # usrpermiss = val[0]


            with open(file=file_path, mode="a", encoding="utf-8") as f:
                f.write(f'{time} {usrname}登录\n')
            print(usrpermiss)
            return HttpResponseRedirect('/system/main.html?name='+usrname+'&permiss='+usrpermiss)
        else:
            return render(request, 'admin/login.html', {'form': form})
    else:
        form = NameForm()
    return render(request, 'admin/login.html', {'form': form})

def register(request):
    if request.method=='POST':
        register_form = forms.RegisterRorm(request.POST)

        message = '请仔细检查填写内容！'
        if register_form.is_valid():
           username = register_form.cleaned_data('username')
           password = register_form.cleaned_data('password')
           password1 = register_form.cleaned_data('password1')
           email = register_form.cleaned_data('email')
           sex = register_form.cleaned_data('sex')

           if password!=password1:
               message = '两次密码输入不同'
               return render(request,'admin/register.html',locals())
           else:
               return render(request,'admin/login.html',locals())
        else:
             return render(request, 'admin/register.html', locals())
    register_form = forms.RegisterRorm()
    return render(request,'admin/register.html',locals())


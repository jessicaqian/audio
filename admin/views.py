# import sqlite3
import configparser
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm


# Create your views here.
def login(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            info = form.cleaned_data
            timenow = datetime.datetime.now()
            T_Now = timenow.minute*60 + timenow.hour * 60*60 + timenow.second
            usrname = info['usrname']
            config = configparser.ConfigParser()
            config.read("conf/admin.ini",encoding='utf-8-sig')
            config.set(usrname, "is_login", 'true')
            config.set(usrname, "t_current", str(T_Now))
            usrpermiss = config.get('usrinfo', usrname)
            config.write(open("conf/admin.ini", "w",encoding='utf-8-sig'))
            return HttpResponseRedirect('/system/main.html?name='+usrname+'&permiss='+usrpermiss)
        else:
            return render(request, 'admin/login.html', {'form': form})
    else:
        form = NameForm()
    return render(request, 'admin/login.html', {'form': form})

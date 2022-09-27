from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import NameForm
# import sqlite3
import configparser
import time,datetime

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
            config.read("admin.ini",encoding='utf-8-sig')
            config.set(usrname, "is_login", 'true')
            config.set(usrname, "t_current", str(T_Now))

            usrpermiss = config.get('usrinfo', usrname)
            config.write(open("admin.ini", "w",encoding='utf-8-sig'))

            # conn = sqlite3.connect('db.sqlite3')
            # cursor = conn.cursor()
            # sql = " SELECT usrpermiss FROM usradmin WHERE usrname='" + usrname + "'"
            # cursor.execute(sql)
            # val = cursor.fetchone()
            # usrpermiss = val[0]
            #print(usrpermiss)
            return HttpResponseRedirect('/system/main.html?name='+usrname+'&permiss='+usrpermiss)
        else:
            return render(request, 'admin/login.html', {'form': form})
    else:
        form = NameForm()
    return render(request, 'admin/login.html', {'form': form})

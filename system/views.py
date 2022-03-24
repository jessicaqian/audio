from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
from .forms import SysconfigForm,UsrForm
import os,sqlite3,hashlib
from . import udp

data = {"cmdCheck": 0x02, "Seq": 0x15,
        "audioPara": {"audioFunc": 0, "audioType": 1, "recordType": 1, "recordTime": 2, "nDevNo": 0, "nCapNo": 0,
                      "mp3Bps": 128, "sampleRate": 48000, "timeInterval": 10, "fileName": "new.mp3",
                      "isStereoSaveFlag": 0}}
udp.senddata(data)
res = udp.getdata(data)
print(res["audioAckValue"]["funcResult"])

# Create your views here.
def main(request):

    if request.method == 'POST':
        pass

    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')

        return render(request, 'system/main.html',{'name':name,'permiss':permiss})

def get_diskstatus(request):
    st = os.statvfs('/home')
    status = st.f_bavail * st.f_frsize/(1024*1024*1024) #这里单位可能差了1024
    no = round(status,2)

    return JsonResponse({'no': no, 'msg': 'success'})#pcm 一个通道：采样率*2*s B  mp3 目标比特率*s bite

def system_config(request):
    if request.method == 'POST':
        pass

    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        form = SysconfigForm()
        return render(request, 'system/sysconfig.html',{'form': form,'name':name,'permiss':permiss})

def usr_config(request):
    if request.method == 'POST':
        pass

    else:
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        sql = " SELECT usrname,usrpermiss FROM usradmin"
        cursor.execute(sql)
        form = cursor.fetchall()
        conn.close()

        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')

        return render(request, 'system/usrconfig.html',{'form': form,'name':name,'permiss':permiss})

def new_usr(request):
    if request.method == 'POST':
        form = UsrForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['usrname']
            password = form.cleaned_data['password_one']
            perssions = form.cleaned_data['usr_perssions']
            u_name = form.cleaned_data['usrname_n']
            u_permiss = form.cleaned_data['usr_perssions_n']
            m = password + "{{sdtzzq}}"
            pw = hashlib.md5(m.encode())

            conn = sqlite3.connect('db.sqlite3')
            cursor = conn.cursor()
            sql = "INSERT INTO usradmin(usrname,psword,usrpermiss) VALUES('"+name+ "','"+pw.hexdigest()+ "','"+perssions+"') "
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return HttpResponseRedirect('/system/usrconfig.html?name='+u_name+'&'+u_permiss)

    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        form = UsrForm()

        return render(request, 'system/newusr.html', { 'form':form,'name': name, 'permiss': permiss})

def dele_usr():

        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        sql = " SELECT usrname,usrpermiss FROM usradmin"
        cursor.execute(sql)
        form = cursor.fetchall()
        conn.close()

        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')

        return render(request, 'system/usrconfig.html',{'form': form,'name':name,'permiss':permiss})

def send_data(request):

    data = {"cmdCheck":0x02,"Seq":0x15,"audioPara":{"audioFunc":1,"audioType":1,"recordType":1,"recordTime":2,"nDevNo":0,"nCapNo":0,
                                                    "mp3Bps":128,"sampleRate":48000,"timeInterval":10,"fileName":"new.mp3","isStereoSaveFlag":0}}
    udp.senddata(data)
    res = udp.getdata(data)
    if res["audioAckValue"]["funcResult"]==0:

        return JsonResponse({ 'msg': 'success'})
    else:
        return JsonResponse({'msg': 'failed'})



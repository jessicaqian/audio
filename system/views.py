from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
from .forms import SysconfigForm,UsrForm
import os,sqlite3,hashlib,json,threading
import time,datetime
from . import udp

# Create your views here.
# data = {"cmdCheck": 0x02, "Seq": 0x15,
#         "audioPara": {"audioFunc": 0, "audioType": 1, "recordType": 0, "recordTime": 20, "nDevNo": 1, "nCapNo": 0,
#                       "mp3Bps": 128, "sampleRate": 48000, "timeInterval": 10, "fileName": "new.mp3",
#                       "isStereoSaveFlag": 0}}
# udp.senddata(data)
# res = udp.getdata(data)
# print(res["audioAckValue"]["funcResult"])

def mkdir():
    threading.Timer(43200,mkdir).start()
    current_time = time.strftime("%Y-%m-%d", time.localtime())
    now_time = datetime.datetime.now()
    lastday_time = (now_time + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
    path = 'static/record/'+current_time
    if not os.path.exists(path):
        os.mkdir(path)
        os.mkdir(path+'/1')
        os.mkdir(path+'/2')
        os.mkdir(path+'/3')
        os.mkdir(path+'/4')
    else:
        pass
    path1 = 'static/record/'+lastday_time
    if not os.path.exists(path1):
        os.mkdir(path1)
        os.mkdir(path1+'/1')
        os.mkdir(path1+'/2')
        os.mkdir(path1+'/3')
        os.mkdir(path1+'/4')
    else:
        pass
    print(lastday_time)

mkdir()


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

def search_mid(request):
    if request.method == 'POST':
        lists = []
        start = request.POST['start']
        start_date = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d')

        start_time = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M').strftime('%H-%M-00')
        end = request.POST['end']
        end_date = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d')
        end_time = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M').strftime('%H-%M-00')
        channel_no = request.POST['no']

        if channel_no == 'all':
            path0 = 'static/record/' + start_date
            if not os.path.exists(path0):
                pass
            else:
                i = 1
                mark = False
                while i < 5:
                    path = 'static/record/' + start_date + '/' + str(i)
                    if not os.listdir(path):
                        pass

                    else:
                        mark = True
                    i = i + 1
                if mark:
                    lists.append(start_date)
        else:
            path0 = 'static/record/' + start_date
            if not os.path.exists(path0):
                pass
            else:
                path = 'static/record/' + start_date + '/' + channel_no
                if not os.listdir(path):
                    pass


                else:
                    lists.append(start_date + '/' + channel_no)

        datestart = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        dateend = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        while datestart < dateend:
            datestart += datetime.timedelta(days=1)
            startdate = datetime.datetime.strftime(datestart, '%Y-%m-%d')
            if channel_no == 'all':
                path0 = 'static/record/' + startdate
                if not os.path.exists(path0):
                    pass
                else:
                    i = 1
                    mark = False
                    while i < 5:
                        path = 'static/record/' + startdate + '/' + str(i)
                        if not os.listdir(path):
                            pass


                        else:
                            mark = True
                        i = i + 1
                    if mark:
                        lists.append(startdate)
            else:
                path0 = 'static/record/' + startdate
                if not os.path.exists(path0):
                    pass
                else:
                    path = 'static/record/' + startdate + '/' + channel_no
                    if not os.listdir(path):
                        pass

                    else:
                        lists.append(startdate + '/' + channel_no)

        print(lists)

        return render(request, 'system/searchmid.html',
                      {'lists': lists, 'start_a': start, 'end_a': end, 'channel_no_a': channel_no})

    else:

        return render(request, 'system/searchmid.html')


def search_time(request):
    lists = []
    start = request.POST['start']
    start_date = datetime.datetime.strptime(start,'%Y-%m-%dT%H:%M').strftime('%Y-%m-%d')

    start_time = datetime.datetime.strptime(start,'%Y-%m-%dT%H:%M').strftime('%H-%M-00')
    end = request.POST['end']
    end_date = datetime.datetime.strptime(end,'%Y-%m-%dT%H:%M').strftime('%Y-%m-%d')
    end_time = datetime.datetime.strptime(end,'%Y-%m-%dT%H:%M').strftime('%H-%M-00')
    channel_no = request.POST['no']

    if channel_no=='all':
        path0 = 'static/record/' + start_date
        if not os.path.exists(path0):
            pass
        else:
            i=1
            mark = False
            while i<5:
                path = 'static/record/' + start_date + '/' + str(i)
                if not os.listdir(path):
                    pass

                else:
                    mark = True
                i = i + 1
            if mark:
                lists.append(start_date)
    else:
        path0 = 'static/record/' + start_date
        if not os.path.exists(path0):
            pass
        else:
            path = 'static/record/' + start_date + '/' + channel_no
            if not os.listdir(path):
                pass


            else:
                lists.append(start_date+ '/' + channel_no)

    datestart = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        startdate = datetime.datetime.strftime(datestart,'%Y-%m-%d')
        if channel_no == 'all':
            path0 = 'static/record/' + startdate
            if not os.path.exists(path0):
                pass
            else:
                i = 1
                mark = False
                while i < 5:
                    path = 'static/record/' + startdate + '/' + str(i)
                    if not os.listdir(path):
                        pass


                    else:
                        mark = True
                    i = i + 1
                if mark:
                    lists.append(startdate)
        else:
            path0 = 'static/record/' + startdate
            if not os.path.exists(path0):
                pass
            else:
                path = 'static/record/' + startdate + '/' + channel_no
                if not os.listdir(path):
                    pass

                else:
                    lists.append(startdate + '/' + channel_no)


    print(lists)


    return render(request, 'system/searchtime.html',
                      {'lists': lists, 'start_a': start, 'end_a': end, 'channel_no_a': channel_no})



def send_data(request):
    data =json.loads(request.POST['mes'])
    print(data)


    udp.senddata(data)
    res = udp.getdata(data)
    if res["audioAckValue"]["funcResult"]==0:

        return JsonResponse({ 'msg': 'success'})
    else:
        return JsonResponse({'msg': 'failed'})

def heartbeat(request):
    res = udp.heartbeat()
    if res==0:
        return JsonResponse({'msg': 'failed'})

    return JsonResponse({'msg': 'success'})




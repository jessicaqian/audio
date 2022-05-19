import pytz
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .forms import SysconfigForm,UsrForm
import os,sqlite3,hashlib,json,threading,re
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

f_lists={}

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

def search_mid(request):
    if request.method == 'POST':
        lists = []
        f_lists.clear()

        start = request.POST['start']
        start_date = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d')

        start_time = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M').strftime('%H%M00')
        end = request.POST['end']
        end_date = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d')
        end_time = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M').strftime('%H%M00')
        channel_no = request.POST['no']

#处理start_date
        if channel_no == 'all':
            path0 = 'static/record/' + start_date
            if not os.path.exists(path0):
                pass
            else:

                i = 1

                while i < 5:
                    path = 'static/record/' + start_date + '/' + str(i)
                    if not os.listdir(path):
                        pass

                    else:
                        mark = False
                        F_lists = []
                        Flists = os.listdir(path)
                        for Flist in Flists:
                            Flist1 = re.sub('.mp3','',Flist)
                            Flist2 = re.sub('-', '', Flist1)
                            Flist_str = list(Flist2)
                            j = 0
                            while j<10:
                                Flist_str.pop(0)
                                j = j + 1
                            Flist3 = ''.join(Flist_str)

                            if start_date == end_date:
                                if (int(start_time)-int(Flist3))<=0 and (int(end_time)-int(Flist3))>=0:
                                    F_lists.append(Flist)
                                    f_lists[start_date + '/' + str(i)] = F_lists
                                    mark = True
                            else:

                                if (int(start_time)-int(Flist3))<=0:
                                    F_lists.append(Flist)
                                    f_lists[start_date + '/' + str(i)] = F_lists
                                    mark = True
                        if mark == True:
                            lists.append(start_date + '/' + str(i))

                    i = i + 1

        else:
            path0 = 'static/record/' + start_date
            if not os.path.exists(path0):
                pass
            else:
                path = 'static/record/' + start_date + '/' + channel_no
                if not os.listdir(path):
                    pass


                else:

                    F_lists = []
                    Flists = os.listdir(path)
                    for Flist in Flists:
                        Flist1 = re.sub('.mp3', '', Flist)
                        Flist2 = re.sub('-', '', Flist1)
                        Flist_str = list(Flist2)
                        j = 0
                        while j < 10:
                            Flist_str.pop(0)
                            j = j + 1
                        Flist3 = ''.join(Flist_str)

                        if (int(start_time) - int(Flist3)) <= 0:
                            F_lists.append(Flist)
                            f_lists[start_date + '/' + channel_no] = F_lists
                    lists.append(start_date + '/' + channel_no)


#处理既不是start_date也不是end_date的中间日期
        datestart = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        dateend = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        if dateend > datestart + datetime.timedelta(days=1):

            while datestart < (dateend + datetime.timedelta(days=-1)):
                datestart += datetime.timedelta(days=1)
                startdate = datetime.datetime.strftime(datestart, '%Y-%m-%d')
                if channel_no == 'all':
                    path0 = 'static/record/' + startdate
                    if not os.path.exists(path0):
                        pass
                    else:
                        i = 1

                        while i < 5:
                            path = 'static/record/' + startdate + '/' + str(i)
                            if not os.listdir(path):
                                pass


                            else:
                                lists.append(startdate + '/' + str(i))

                            i = i + 1


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

#处理end_data
        datestart = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        dateend = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        if dateend >= datestart + datetime.timedelta(days=1):
            if channel_no == 'all':
                path0 = 'static/record/' + end_date
                if not os.path.exists(path0):
                    pass
                else:

                    i = 1

                    while i < 5:
                        path = 'static/record/' + end_date + '/' + str(i)
                        if not os.listdir(path):
                            pass

                        else:
                            mark = False
                            F_lists = []
                            Flists = os.listdir(path)
                            for Flist in Flists:
                                Flist1 = re.sub('.mp3', '', Flist)
                                Flist2 = re.sub('-', '', Flist1)
                                Flist_str = list(Flist2)
                                j = 0
                                while j < 10:
                                    Flist_str.pop(0)
                                    j = j + 1
                                Flist3 = ''.join(Flist_str)

                                if (int(end_time) - int(Flist3)) >= 0:
                                    F_lists.append(Flist)
                                    f_lists[end_date + '/' + str(i)] = F_lists
                                    mark = True
                            if mark == True:
                                lists.append(end_date + '/' + str(i))

                        i = i + 1

            else:
                path0 = 'static/record/' + end_date
                if not os.path.exists(path0):
                    pass
                else:
                    path = 'static/record/' + end_date + '/' + channel_no
                    if not os.listdir(path):
                        pass


                    else:

                        F_lists = []
                        Flists = os.listdir(path)
                        for Flist in Flists:
                            Flist1 = re.sub('.mp3', '', Flist)
                            Flist2 = re.sub('-', '', Flist1)
                            Flist_str = list(Flist2)
                            j = 0
                            while j < 10:
                                Flist_str.pop(0)
                                j = j + 1
                            Flist3 = ''.join(Flist_str)

                            if (int(end_time) - int(Flist3)) >= 0:
                                F_lists.append(Flist)
                                f_lists[end_date + '/' + channel_no] = F_lists
                        lists.append(end_date + '/' + channel_no)





        return render(request, 'system/searchmid.html',
                      {'lists': lists, 'start_a': start, 'end_a': end, 'channel_no_a': channel_no,'mark':'post','start_data':start_date,'end_data':end_date})

    else:

        return render(request, 'system/searchmid.html')

def audio_file(request):
    if request.method == 'POST':
        pass

    else:


        dir = request.GET.get('dir', default='10000000')
        try:
            print(f_lists[dir])
            path = 'static/record/' + dir
            lists = f_lists[dir]
        except:
            path = 'static/record/' + dir
            lists =  os.listdir(path)
        return render(request, 'system/audiofile.html', {'lists': lists, 'path': path})


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



#
# """
# 日志信息
# yxy
#添加日志
# """
def free_logs(request):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    if request.method == 'POST':
        data =json.loads(request.POST['mes'])
        start_time = data.get('start_time')
        end_time = data.get("end_time")
        user_name = data.get("name")
        channel_name = data.get("channel_name")
        sql = "SELECT id FROM audio_logs limit 1 offset (select COUNT (id) -1 FROM audio_logs)"
        cursor.execute(sql)
        array = cursor.fetchall()
        json_dict = {}
        for i in array:
            json_dict["id"] = i[0]
        data = json_dict.get('id')
        if end_time is None:
            sql = "INSERT INTO audio_logs(start_time,user_name,channel_name) values ({},'{}','{}')".format(start_time, user_name,channel_name)
            cursor.execute(sql)
            conn.commit()
        else:
            sql = f"UPDATE audio_logs SET end_time = '{end_time}' where id={data} "
            cursor.execute(sql)
            conn.commit()
        conn.close()
        return JsonResponse({'mes':"ok"})
    else:
        return render(request,'system/free.html')

#获取时间戳和分页内的日志
def free(request):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    if request.method == "POST":
        pass
    else:
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")
        start = request.GET.get("start_time")
        end = request.GET.get("end_time")
        timestrs =start.replace('T', ' ')
        timestre =end.replace('T', ' ')
        times = time.strptime(timestrs,"%Y-%m-%d %H:%M")
        timee = time.strptime(timestre,"%Y-%m-%d %H:%M")
        st = int(time.mktime(times))
        et = int(time.mktime(timee))

        if limit is not None:
            sql = f"SELECT start_time,end_time,channel_name,user_name FROM audio_logs where start_time between {st} and {et} limit {limit} "
            cursor.execute(sql)
        if offset is not None:
            sql = "SELECT start_time,end_time,channel_name,user_name FROM audio_logs limit {} offset {}".format(st,et,limit,offset)
            cursor.execute(sql)

        array = cursor.fetchall()
        conn.close()
        status_dict = []
        for i in array:
            status_dict.append({
                "start_time":i[0],
                "ent_time":i[1],
                'channel_name':i[2],
                'user_name':i[3],
            })
        return JsonResponse({'list':status_dict})

# 这个主要是返回html模板
def free_html(request):
    if request.method=="POST":
        pass
    else:
        return render(request,'system/free.html')
# 这里是获取时间戳内的日志总数,用于计算分页
def free_count(request):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    if request.method=="POST":
        pass
    else:
        start = request.GET.get("start_time")
        end = request.GET.get("end_time")
        timestrs = start.replace('T', ' ')
        timestre = end.replace('T', ' ')
        times = time.strptime(timestrs, "%Y-%m-%d %H:%M")
        timee = time.strptime(timestre, "%Y-%m-%d %H:%M")
        st = int(time.mktime(times))
        et = int(time.mktime(timee))
        sql = "SELECT count(id) FROM audio_logs"
        cursor.execute(sql)

        array = cursor.fetchone()
        json_count =json.dumps(array)
        print(array)
        conn.close()
        return HttpResponse(json_count)

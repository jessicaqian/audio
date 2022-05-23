import pytz
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .forms import SysconfigForm,UsrForm
import os,sqlite3,hashlib,json,threading,re
import time,datetime,configparser
from . import udp


# Create your views here.
# data = {"cmdCheck": 0x02, "Seq": 0x15,
#         "audioPara": {"audioFunc": 0, "audioType": 1, "recordType": 0, "recordTime": 20, "nDevNo": 1, "nCapNo": 0,
#                       "mp3Bps": 128, "sampleRate": 48000, "timeInterval": 10, "fileName": "new.mp3",
#                       "isStereoSaveFlag": 0}}
# udp.senddata(data)
# res = udp.getdata(data)
# print(res["audioAckValue"]["funcResult"])
dir = os.getcwd()
file_path = dir + '/audio_logs.txt'

f_lists={}
config = configparser.ConfigParser()

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
        config.read("web.ini")
        audiomode = config.get("configinfo", "audiomode")
        channel1 =  config.get("configinfo", "channel1")
        channel2 =  config.get("configinfo", "channel2")
        channel3 = config.get("configinfo", "channel3")
        channel4 =  config.get("configinfo", "channel4")
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        with open(file=file_path, mode="a", encoding="utf-8") as f:
            f.write(f'{time} {name}登录\n')
        return render(request, 'system/main.html',{'name':name,'permiss':permiss,'channel1':channel1,'channel2':channel2,'channel3':channel3,'channel4':channel4,'audiomode':audiomode})

def get_diskstatus(request):
    st = os.statvfs('/home')
    status = st.f_bavail * st.f_frsize/(1024*1024*1024) #这里单位可能差了1024
    no = round(status,2)

    return JsonResponse({'no': no, 'msg': 'success'})#pcm 一个通道：采样率*2*s B  mp3 目标比特率*s bite

def system_config(request):
    config.read("web.ini")
    if request.method == 'POST':
        form = SysconfigForm(request.POST)
        if form.is_valid():
            audiotype = form.cleaned_data['audiotype']
            audiomode = form.cleaned_data['audiomode']
            if audiomode == '全时段录音':
                audiotime = form.cleaned_data['audiotime']
                config.set("configinfo", "audiotime", audiotime)

            channel1 = form.cleaned_data['channel1']
            channel2 = form.cleaned_data['channel2']
            channel3 = form.cleaned_data['channel3']
            channel4 = form.cleaned_data['channel4']

            config.set("configinfo","audiotype",audiotype)
            config.set("configinfo", "audiomode", audiomode)

            config.set("configinfo", "channel1", channel1)
            config.set("configinfo", "channel2", channel2)
            config.set("configinfo", "channel3", channel3)
            config.set("configinfo", "channel4", channel4)
            config.write(open("web.ini","w"))
            print(form)
            return render(request, 'system/sysconfig.html', {'form': form})
        else:

            return render(request, 'system/sysconfig.html', {'form': form})


    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        form = SysconfigForm()
        audiotype = config.get("configinfo","audiotype")
        audiomode =  config.get("configinfo", "audiomode")
        audiotime =  config.get("configinfo", "audiotime")
        channel1 =  config.get("configinfo", "channel1")
        channel2 =  config.get("configinfo", "channel2")
        channel3 = config.get("configinfo", "channel3")
        channel4 =  config.get("configinfo", "channel4")


        return render(request, 'system/sysconfig.html',{'form': form,'method':'get','name':name,'permiss':permiss,'audiotype':audiotype,'audiomode':audiomode,
                                                        'audiotime':audiotime,'channel1':channel1,'channel2':channel2,'channel3':channel3,'channel4':channel4})

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
    if request.method == 'POST':
        data =json.loads(request.POST['mes'])
        start_time = data.get('start_time')
        end_time = data.get("end_time")
        user_name = data.get("name")
        channel_name = data.get("channel_name")
        if end_time is None:
            with open(file=file_path, mode="a", encoding="utf-8") as f:
                f.write(f'{start_time} {channel_name} {user_name}开始录音\n')
        else:
            with open(file=file_path, mode="a", encoding="utf-8") as f:
                f.write(f'{end_time} {channel_name} {user_name}停止录音\n')
        return JsonResponse({'mes':"ok"})
    else:
        return render(request,'system/free.html')



# 这个主要是返回html模板
def free_html(request):
    if request.method=="POST":
        pass
    else:
        return render(request,'system/free.html')
# 这里现在是查询展示日志的功能，
def free_count(request):
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    if request.method=="POST":
        pass
    else:

        page_num = request.GET.get('page',1)
        with open(file=file_path, mode="r", encoding="utf-8") as f:
            data =f.read().splitlines()
        #     print(data)
        paginator = Paginator(data, 5)
        # if page_num is not None:
        #     c_page = paginator.page(int(page_num))
        # else:
        #     c_page = paginator.page(int(page_num))
        try:
            # print(page)
            book_list = paginator.page(int(page_num))  # 获取当前页码的记录
        except PageNotAnInteger:
            book_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
        except EmptyPage:
            book_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容

        return render(request,'system/free.html',locals())

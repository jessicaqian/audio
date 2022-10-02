from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from .forms import SysconfigForm,UsrForm,NetForm,UsreditForm
import os,hashlib,json,threading,re
import time,datetime,configparser
from . import udp
from ctypes import *

# Create your views here.

target = cdll.LoadLibrary("./pcmToWavqq.so")
s_show = cdll.LoadLibrary("./usbtty_neokylin.so")

s_show.main()

time.time()
now = datetime.datetime.now()
timestr = now.strftime("%Y-%m-%d")
dir = os.getcwd() + '/logs'
if not os.path.exists(dir):
    os.mkdir(dir)
file_path = dir + '/'+timestr+'.txt'

f_lists={}

config = configparser.ConfigParser()
config1 = configparser.ConfigParser()
config.read("web.ini")
pw = config.get("systeminfo", "syspw")
mpath = config.get("systeminfo", "mpath")


r_status = ['off','off','off','off']
modedict={'mp3':1,'wav':0,'全时段录音':0,'自动录音':1}##


def init():

    audiomode = config.get("configinfo", "audiomode")
    audiotype = config.get("configinfo", "audiotype")
    audiotime = config.get("configinfo", "audiotime")
    ip = config.get("systeminfo", "inip")


    data = {"cmdCheck": 0x02, "Seq": 0x15,
            "audioPara": {"audioFunc": 3, "audioType": modedict[audiotype], "recordType": modedict[audiomode], "recordTime": int(audiotime), "nDevNo": 1, "nCapNo": 0,
                          "mp3Bps": 128, "sampleRate": 48000, "timeInterval": 10, "fileName": "10.25.15.167:/home/zzq/PycharmProjects/audio_record/static/record/",
                          "isStereoSaveFlag": 0}}
    try:
        udp.senddata(data)
        res = udp.getdata()
        print(res)

    except:
        print('stop error')




    data = {"cmdCheck": 0x02, "Seq": 0x15,
            "audioPara": {"audioFunc": 0, "audioType": modedict[audiotype], "recordType": modedict[audiomode], "recordTime": int(audiotime), "nDevNo": 1, "nCapNo": 0,
                          "mp3Bps": 128, "sampleRate": 48000, "timeInterval": 10, "fileName": "10.25.15.167:/home/zzq/PycharmProjects/audio_record/static/record/",
                          "isStereoSaveFlag": 0}}
    try:
        udp.senddata(data)
        res = udp.getdata()
        print(res)

    except:
        print('start error')

    data = {"cmdCheck": 0x02, "Seq": 0x15,
            "audioPara": {"audioFunc": 5, "audioType": modedict[audiotype], "recordType": modedict[audiomode], "recordTime": int(audiotime), "nDevNo": 1, "nCapNo": 0,
                          "mp3Bps": 128, "sampleRate": 48000, "timeInterval": 10, "fileName": ip+":"+mpath,
                          "isStereoSaveFlag": 0}}
    try:
        udp.senddata(data)
        res = udp.getdata()
        print(res)

    except:
        print('mount error')


def sudoCMD(command,password):
    str = os.system('echo %s | sudo -S %s' % (password,command))
    print(str)

def pcmtowav(input,output):  #pcm转wav

    file1 = bytes(input, encoding='utf-8')
    file2 = bytes(output, encoding='utf-8')

    try:

        no = target.swich(file1, file2)
        print(no)
        sudoCMD('rm -f '+ input,pw)
        return 1
    except:
        return 0

def checkpcm(ch_no):  #检查pcm文件
    current_time = time.strftime("%Y-%m-%d", time.localtime()) #获取当前时间
    path = mpath + current_time + '/' + ch_no + '/' #文件存储路径
    lists = os.listdir(path) #路径文件列表
    sudoCMD('chmod 777 -R ' + path, pw)
    for list in lists:
        if ('pcm' in list):
            list0 = re.sub('.pcm', '', list) + '.wav'
            pcmtowav(path+list,path+list0)


def login_required(func):  # 自定义登录验证装饰器
    def warpper(request, *args, **kwargs):
        timenow = datetime.datetime.now()
        T_Now = timenow.minute + timenow.hour * 60
        config.read("web.ini")

        name = request.GET.get('name', default='e')
        if name == 'e':
            return HttpResponseRedirect("/") #没有名字，直接跳转登录页
        else:
            try:

                T_logout = int(config.get(name,'T_current')) #名字正确继续执行
                interval = int(T_Now - T_logout)
                if interval>30:
                    config.set(name,'is_login','false')
                else:
                    config.set(name, 'T_current',str(T_Now))
                config.write(open("web.ini", "w"))
            except:
                return HttpResponseRedirect("/")
        is_login = config.get(name,'is_login')

        if is_login == 'true':
            return func(request, *args, **kwargs)
        else:

            return HttpResponseRedirect("/")
    return warpper

def mkdir():
    threading.Timer(43200,mkdir).start()
    current_time = time.strftime("%Y-%m-%d", time.localtime())
    now_time = datetime.datetime.now()
    lastday_time = (now_time + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
    path = mpath+current_time
    if not os.path.exists(path):
        os.mkdir(path)
        os.mkdir(path+'/1')
        os.mkdir(path+'/2')
        os.mkdir(path+'/3')
        os.mkdir(path+'/4')
    else:
        pass
    path1 = mpath+lastday_time
    if not os.path.exists(path1):
        os.mkdir(path1)
        os.mkdir(path1+'/1')
        os.mkdir(path1+'/2')
        os.mkdir(path1+'/3')
        os.mkdir(path1+'/4')
    else:
        pass

#######################################start here######################################################################
init()
mkdir()

@login_required
def main(request):

    if request.method == 'POST':
        pass

    else:
        # config.read("web.ini")
        audiomode = config.get("configinfo", "audiomode")
        audiotype = config.get("configinfo","audiotype")
        channel1 =  config.get("configinfo", "channel1")
        channel2 =  config.get("configinfo", "channel2")
        channel3 = config.get("configinfo", "channel3")
        channel4 =  config.get("configinfo", "channel4")
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        # with open(file=file_path, mode="a", encoding="utf-8") as f:
        #     f.write(f'{time} {name}登录\n')

        return render(request, 'system/main.html',locals())

def get_diskstatus(request):
    st = os.statvfs('/home')
    status = st.f_bavail * st.f_frsize/(1024*1024*1024)
    no = round(status,2)
    time = round(st.f_bavail * st.f_frsize/(60*60*16),2)


    return JsonResponse({'no': no, 'msg': 'success','time':time})#pcm 一个通道：采样率*2*s B  mp3 目标比特率*s bite

def record_status(request):
    if request.method == 'POST':
        strno = request.POST['no']
        no = int(strno)-1
        act = request.POST['act']
        r_status[no] = act
        if act == 'off':
            checkpcm(strno)

    else:
        pass
    return JsonResponse({'msg': 'success'})

@login_required
def system_config(request):
    config.read("web.ini")
    if request.method == 'POST':
        form = SysconfigForm(request.POST)
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        if form.is_valid():

            u_name = form.cleaned_data['usrname_n']
            u_permiss = form.cleaned_data['usr_perssions_n']

            audiotype = form.cleaned_data['audiotype']
            audiomode = form.cleaned_data['audiomode']
            audiotime = form.cleaned_data['audiotime']

            raudiotype = config.get("configinfo", "audiotype")
            raudiomode = config.get("configinfo", "audiomode")
            raudiotime = config.get("configinfo", "audiotime")

            if audiotype == raudiotype and audiomode== raudiomode and audiotime == raudiotime:
                pass
            else:

                data = {"cmdCheck": 0x02, "Seq": 0x15,
                        "audioPara": {"audioFunc": 3, "audioType": modedict[audiotype], "recordType": modedict[audiomode], "recordTime": int(audiotime), "nDevNo": 1,
                                      "nCapNo": 0,
                                      "mp3Bps": 128, "sampleRate": 48000, "timeInterval": 10,
                                      "fileName": "10.25.15.167:/home/zzq/PycharmProjects/audio_record/static/record/",
                                      "isStereoSaveFlag": 0}}
                try:
                    udp.senddata(data)
                    res = udp.getdata()
                    print(res)
                    if res == 0:
                        return render(request, 'system/sysconfig.html',{'form': form, 'name': u_name, 'permiss': u_permiss, 'audiotype': raudiotype,'audiomode': raudiomode, 'audiotime': raudiotime,'res':'failed'})
                except:
                    print('systemconfig stop error')
                    return render(request, 'system/sysconfig.html',{'form': form, 'name': u_name, 'permiss': u_permiss, 'audiotype': raudiotype,'audiomode': raudiomode, 'audiotime': raudiotime, 'res': 'failed'})
                i = 0
                while i<4:
                    r_status[i]='off'
                    i = i+1

                data = {"cmdCheck": 0x02, "Seq": 0x15,
                        "audioPara": {"audioFunc": 0, "audioType": modedict[audiotype], "recordType": modedict[audiomode], "recordTime": int(audiotime), "nDevNo": 1,
                                      "nCapNo": 0,
                                      "mp3Bps": 128, "sampleRate": 48000, "timeInterval": 10,
                                      "fileName": "10.25.15.167:/home/zzq/PycharmProjects/audio_record/static/record/",
                                      "isStereoSaveFlag": 0}}


                try:
                    udp.senddata(data)
                    res = udp.getdata()
                    print(res)
                    if res == 0:
                        return render(request, 'system/sysconfig.html',{'form': form, 'name': u_name, 'permiss': u_permiss, 'audiotype': raudiotype,'audiomode': raudiomode, 'audiotime': raudiotime, 'res': 'failed'})
                    else:
                        config.set("configinfo", "audiotype", audiotype)
                        config.set("configinfo", "audiomode", audiomode)
                        config.set("configinfo", "audiotime", audiotime)
                        with open(file=file_path, mode="a", encoding="utf-8") as f:
                            f.write(f'{time} {u_name}用户 将存储格式:{raudiotype}修改为存储格式{audiotype}; 录音模式：{raudiomode}修改为录音模式：'
                                    f'{audiomode}; 存储时间:{raudiotime}分钟修改为存储时间:{audiotime}分钟\n')
                except:
                    print('systemconfig restart error')
                    return render(request, 'system/sysconfig.html',{'form': form, 'name': u_name, 'permiss': u_permiss, 'audiotype': raudiotype,'audiomode': raudiomode, 'audiotime': raudiotime, 'res': 'failed'})

            wchannel1 = form.cleaned_data['channel1']
            wchannel2 = form.cleaned_data['channel2']
            wchannel3 = form.cleaned_data['channel3']
            wchannel4 = form.cleaned_data['channel4']
            rchannel1 = config.get("configinfo", "channel1")
            rchannel2 = config.get("configinfo", "channel2")
            rchannel3 = config.get("configinfo", "channel3")
            rchannel4 = config.get("configinfo", "channel4")

            config.set("configinfo", "channel1", wchannel1)
            config.set("configinfo", "channel2", wchannel2)
            config.set("configinfo", "channel3", wchannel3)
            config.set("configinfo", "channel4", wchannel4)
            config.write(open("web.ini","w"))


            with open(file=file_path, mode="a", encoding="utf-8") as f:
                f.write(f'{time} {u_name}用户 将通道一:{rchannel1}修改为通道一:{wchannel1}; 通道二:{rchannel2}修改为通道二:{wchannel2}; 通道三:{rchannel3}修改为通道三:{wchannel3}; 通道四:{rchannel4}修改为{wchannel4}\n')

            return render(request, 'system/sysconfig.html', {'form': form,'name':u_name,'permiss':u_permiss,'audiotype':audiotype,'audiomode':audiomode,'audiotime':audiotime,'res':'success'})
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
        if permiss == '管理员':
            return render(request, 'system/sysconfig.html',{'form': form,'method':'get','name':name,'permiss':permiss,'audiotype':audiotype,'audiomode':audiomode,
                                                        'audiotime':audiotime,'channel1':channel1,'channel2':channel2,'channel3':channel3,'channel4':channel4})
        else:
            return render(request, 'system/error.html',{'name':name,'permiss':permiss,'ecode':0})

@login_required
def net_config(request):
    if request.method == 'POST':
        form = NetForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['usrname_n']
            permiss = form.cleaned_data['usr_perssions_n']
            ip = form.cleaned_data['ip']
            mask = form.cleaned_data['mask']
            gateway = form.cleaned_data['netgate']
            config.read("web.ini")
            dev = config.get("systeminfo", "netdev")
            pw = config.get("systeminfo", "syspw")
            path0 = config.get("systeminfo", "path")
            path = path0+ dev
            sudoCMD('chmod 777 '+ path,pw)
            sudoCMD('touch ' + path+'cp', pw)
            sudoCMD('chmod 777 ' + path+'cp', pw)
            try:
                with open(path+'cp', mode='w', encoding='utf-8') as fw, open(path, mode='r', encoding='utf-8') as fr:
                    for line in fr:
                        if 'BOOTPROTO' in line:
                            line = 'BOOTPROTO=static\n'
                        elif 'ONBOOT' in line:
                            line = 'ONBOOT=yes\n'
                        elif 'GATEWAY' in line:
                            line = 'GATEWAY='+gateway+'\n'
                        elif 'IPADDR' in line:
                            line = 'IPADDR='+ip+'\n'
                        elif 'NETMASK' in line:
                            line = 'NETMASK='+mask+'\n'
                        fw.write(line)
                fr.close()
                fw.close()
                with open(path+'cp', mode='r', encoding='utf-8') as fr1, open(path, mode='w', encoding='utf-8') as fw1:
                    for line in fr1:
                        fw1.write(line)
                fr1.close()
                fw1.close()
                try:
                    config.set("systeminfo", "ip", ip)
                    config.set("systeminfo", "mask", mask)
                    config.set("systeminfo", "gateway", gateway)
                    config.write(open("web.ini", "w"))
                except:
                    pass
                sudoCMD('reboot', pw)
                return render(request, 'system/netconfig.html', {'name': name, 'permiss': permiss})
            except:

                return render(request, 'system/netconfig.html',{'name':name,'permiss': permiss,'ip':ip,'mask':mask,'gateway':gateway})
    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        form = NetForm()
        ip = config.get("systeminfo", "ip")
        mask = config.get("systeminfo", "mask")
        gateway = config.get("systeminfo", "gateway")
        return render(request, 'system/netconfig.html', {'name': name, 'permiss': permiss, 'form': form,'ip':ip,'mask':mask,'gateway':gateway})

@login_required
def usr_config(request):
    if request.method == 'POST':
        pass

    else:
        config.read("web.ini")
        usrinfo = config.items('usrinfo')
        # print(usrinfo)

        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        if permiss == '管理员':

            return render(request, 'system/usrconfig.html',{'name':name,'permiss':permiss,'usrinfo':usrinfo})
        else:
            return render(request, 'system/error.html',{'name':name,'permiss':permiss,'ecode':0})

@login_required
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

            config.read("web.ini")
            try:
                config.add_section(name)
                config.set(name, "name", name)
                config.set(name, "pw", pw.hexdigest())
                config.set("usrinfo", name, perssions)
                config.write(open("web.ini", "w"))

                now = datetime.datetime.now()
                time = now.strftime("%Y-%m-%d %H:%M:%S")
                with open(file=file_path, mode="a", encoding="utf-8") as f:
                    f.write(f'{time} {u_name}用户 新建用户{name}权限:{perssions}\n')
                return HttpResponseRedirect('/system/usrconfig.html?name='+u_name+'&permiss='+u_permiss)

            except:
                return render(request, 'system/error.html', {'name': u_name, 'permiss': u_permiss,'ecode':1})

    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        form = UsrForm()
        if permiss == '管理员':

            return render(request, 'system/newusr.html', { 'form':form,'name': name, 'permiss': permiss})
        else:
            return render(request, 'system/error.html',{'name':name,'permiss':permiss,'ecode':0})

@login_required
def del_usr(request):

        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        usrname = request.GET.get('usrname')
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        with open(file=file_path, mode="a", encoding="utf-8") as f:
            f.write(f'{time} {name}用户 删除用户{usrname}权限:{permiss}\n')



        config.read("web.ini")
        config.remove_section(usrname)
        config.remove_option("usrinfo",usrname)

        config.write(open("web.ini", "w"))

        return HttpResponseRedirect('/system/usrconfig.html?name='+name+'&permiss='+permiss)


def remote_control(request):
    if request.method == 'POST':
        config.read("web.ini")
        pw = config.get("systeminfo", "syspw")
        method = request.POST.get('mark')

        data = {"cmdCheck": 0x02, "Seq": 0x15,
                "audioPara": {"audioFunc": 3, "audioType":0, "recordType": 0,
                              "recordTime": 0, "nDevNo": 1, "nCapNo": 0,
                              "mp3Bps": 128, "sampleRate": 48000, "timeInterval": 10,
                              "fileName": "10.25.15.167:/home/zzq/PycharmProjects/audio_record/static/record/",
                              "isStereoSaveFlag": 0}}
        try:
            udp.senddata(data)
            res = udp.getdata()
            print(res)

        except:
            print('stop error')

        if method == 'shutdown':
            sudoCMD('shutdown', pw)
        if method == 'reboot':
            sudoCMD('reboot', pw)
        return JsonResponse({'msg': 'success'})

    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        return render(request, 'system/remotectr.html', {'name': name, 'permiss': permiss, 'ecode': 0})


@login_required
def search_mid(request):
    config.read("web.ini")
    chan_list=[]
    num =1
    while num<5:
        channel = config.get("configinfo", "channel"+str(num))
        chan_list.append(channel)
        num = num+1
    # print(chan_list)

    if request.method == 'POST':
        lists = []
        f_lists.clear()

        name = request.POST['usrname_n']
        permiss = request.POST['usr_perssions_n']

        start = request.POST['start']
        start_date = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d')
        start_time = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M').strftime('%H%M00')
        end = request.POST['end']
        end_date = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d')
        end_time = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M').strftime('%H%M00')
        channel_no = request.POST['no']

#处理start_date
        if channel_no == 'all':
            path0 = mpath + start_date
            if not os.path.exists(path0):
                pass
            else:

                i = 1

                while i < 5:
                    path = mpath + start_date + '/' + str(i)
                    if not os.listdir(path):
                        pass

                    else:
                        mark = False
                        F_lists = []
                        Flists = os.listdir(path)
                        for Flist in Flists:
                            Flist1 = re.sub('.mp3','',Flist)
                            Flist0 = re.sub('.wav','',Flist1)
                            Flist2 = re.sub('-', '', Flist0)
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
            path0 = mpath + start_date
            if not os.path.exists(path0):
                pass
            else:
                path = mpath + start_date + '/' + channel_no
                if not os.listdir(path):
                    pass


                else:

                    F_lists = []
                    Flists = os.listdir(path)
                    for Flist in Flists:
                        Flist1 = re.sub('.mp3', '', Flist)
                        Flist0 = re.sub('.wav', '', Flist1)
                        Flist2 = re.sub('-', '', Flist0)
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
                    path0 = mpath + startdate
                    if not os.path.exists(path0):
                        pass
                    else:
                        i = 1

                        while i < 5:
                            path = mpath + startdate + '/' + str(i)
                            if not os.listdir(path):
                                pass


                            else:
                                lists.append(startdate + '/' + str(i))

                            i = i + 1


                else:
                    path0 = mpath + startdate
                    if not os.path.exists(path0):
                        pass
                    else:
                        path = mpath + startdate + '/' + channel_no
                        if not os.listdir(path):
                            pass

                        else:
                            lists.append(startdate + '/' + channel_no)

#处理end_data
        datestart = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        dateend = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        if dateend >= datestart + datetime.timedelta(days=1):
            if channel_no == 'all':
                path0 = mpath + end_date
                if not os.path.exists(path0):
                    pass
                else:

                    i = 1

                    while i < 5:
                        path = mpath + end_date + '/' + str(i)
                        if not os.listdir(path):
                            pass

                        else:
                            mark = False
                            F_lists = []
                            Flists = os.listdir(path)
                            for Flist in Flists:
                                Flist1 = re.sub('.mp3', '', Flist)
                                Flist0 = re.sub('.wav', '', Flist1)
                                Flist2 = re.sub('-', '', Flist0)
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
                path0 = mpath + end_date
                if not os.path.exists(path0):
                    pass
                else:
                    path = mpath + end_date + '/' + channel_no
                    if not os.listdir(path):
                        pass


                    else:

                        F_lists = []
                        Flists = os.listdir(path)
                        for Flist in Flists:
                            Flist1 = re.sub('.mp3', '', Flist)
                            Flist0 = re.sub('.wav','',Flist1)
                            Flist2 = re.sub('-', '', Flist0)
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
                      {'name':name,'permiss':permiss,'lists': lists, 'start_a': start, 'end_a': end, 'channel_no_a': channel_no,'mark':'post','start_data':start_date,'end_data':end_date,'chanlist':chan_list})

    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')

        pw = config.get("systeminfo", "syspw")
        path = 'static/record'
        sudoCMD('chmod 777 -R ' + path, pw)

        return render(request, 'system/searchmid.html',{'name':name,'permiss':permiss,'chanlist':chan_list})

@login_required
def audio_file(request):
    if request.method == 'POST':
        pass

    else:


        dir = request.GET.get('dir', default='10000000')
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        try:
            # print(f_lists[dir])
            path = mpath + dir
            lists = f_lists[dir]
        except:
            path = mpath + dir
            lists =  os.listdir(path)
        return render(request, 'system/audiofile.html', {'lists': lists, 'path': path,'name':name,'permiss':permiss})


def send_data(request):
    data =json.loads(request.POST['mes'])
    # print(data)

    udp.senddata(data)
    res = udp.getdata()
    if res == 0:
        return JsonResponse({'msg': 'failed'})

    return JsonResponse({'msg': 'success'})

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
        channel_no = data.get("channel_no")
        channel_name = data.get("channel_name")
        if end_time is None:
            with open(file=file_path, mode="a", encoding="utf-8") as f:
                f.write(f'{start_time} 用户:{user_name}开始录音 通道号:{channel_no} 通道名:{channel_name}\n')
        else:
            with open(file=file_path, mode="a", encoding="utf-8") as f:
                f.write(f'{end_time} 用户:{user_name}停止录音 通道号:{channel_no} 通道名:{channel_name}\n')
        return JsonResponse({'mes':"ok"})
    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        return render(request,'system/free.html',{'name':name,'permiss':permiss})



# 这个主要是返回html模板
def free_html(request):
    if request.method=="POST":
        pass
    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        return render(request,'system/free.html',{'name':name,'permiss':permiss})
# 这里现在是查询展示日志的功能，
def free_count(request):

    if request.method=="POST":
        pass

    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        page_num = request.GET.get('page',1)
        st = request.GET.get('start')
        et = request.GET.get('end')
        if st is not None and et is not None:

            page_num = request.GET.get('page', 1)
            listdivd =[]
            listdir =os.listdir(dir)
            for i in listdir:
                time_os = i[0:10]
                if time_os >= st and time_os<=et:
                    with open(file=dir+'/'+i, mode="r", encoding="utf-8") as f:
                        data =f.readlines()
                        listdivd.extend(data)

            paginator = Paginator(listdivd, 25)
            try:
                # print(page)
                book_list = paginator.page(int(page_num))  # 获取当前页码的记录
            except PageNotAnInteger:
                book_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
            except EmptyPage:
                book_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页`码列表中时,显示最后一页的内容

            return render(request,'system/free.html',{'name':name,'permiss':permiss,'start':st,'end':et,'mark':'reload','page_num':page_num,'locals':locals()})
        else:
            return render(request, 'system/free.html',{'name': name, 'permiss': permiss})





def devices(request):
    if request.method =="POST":
        pass
    else:
        config.read("web.ini")

        audiotype = config.get("configinfo", "audiotype")
        channel1 = config.get("configinfo", "channel1")
        channel2 = config.get("configinfo", "channel2")
        channel3 = config.get("configinfo", "channel3")
        channel4 = config.get("configinfo", "channel4")
        listd={"data":
                [{"id":"1",
                "name":channel1,
                "status":r_status[0],
                "fileType":audiotype
                },
               {"id":"2",
                "name":channel2,
                "status":r_status[1],
                "fileType":audiotype},
               {"id":"3",
                "name":channel3,
                "status":r_status[2],
                "fileType":audiotype},
               {"id":"4",
                "name":channel4,
                "status":r_status[3],
                "fileType":audiotype}]}
    return JsonResponse(listd)

@login_required
def edit_usr(request):
    if request.method == 'POST':
        form = UsreditForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['usrname']
            password = form.cleaned_data['password_one']
            n_password = form.cleaned_data['password_two']
            u_name = form.cleaned_data['usrname_n']
            u_permiss = form.cleaned_data['usr_perssions_n']
            m = password + "{{sdtzzq}}"
            pw = hashlib.md5(m.encode())

            config1.read("admin.ini",encoding='utf-8-sig')

            pw_conf = config1.get(name,"pw")
            if pw.hexdigest() == pw_conf:
                m1 = n_password + "{{sdtzzq}}"
                pw1 = hashlib.md5(m1.encode())
                config1.set(name, "pw", pw1.hexdigest())

                config1.write(open("admin.ini", "w",encoding='utf-8-sig'))

                now = datetime.datetime.now()
                time = now.strftime("%Y-%m-%d %H:%M:%S")
                # with open(file=file_path, mode="a", encoding="utf-8") as f:
                #     f.write(f'{time} {u_name}用户 新建用户{name}权限:{perssions}\n')
                return HttpResponseRedirect('/system/usrconfig.html?name='+u_name+'&permiss='+u_permiss)
            else:
                return render(request,'system/usredit.html',{'form':form,'name':u_name,'permiss':u_permiss,'method':'error'})

    else:
        form = UsreditForm()
        usrname = request.GET.get('usrname')
        usrpermiss = request.GET.get('usrpermiss')
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        if permiss == '管理员':

            return render(request, 'system/usredit.html', {'name': name, 'permiss': permiss, 'form': form,'usrname':usrname,'usrpermiss':usrpermiss,'method':'get'})
        else:
            return render(request, 'system/error.html', {'name': name, 'permiss': permiss, 'ecode': 0})

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from .forms import SysconfigForm,UsrForm,NetForm,ChannelForm
import os,hashlib,json,re
import time,datetime,configparser,requests
import ctypes

time.time()
now = datetime.datetime.now()
timestr = now.strftime("%Y-%m-%d")

dir = os.getcwd() + '/logs'
if not os.path.exists(dir):
    os.mkdir(dir)
file_path = dir + '/'+timestr+'.txt'
print(file_path)

f_lists={}
config = configparser.ConfigParser()

r_status = ['off']*64

def sudoCMD(command,password):
    str = os.system('echo %s | sudo -S %s' % (password,command))
    print(str)

def login_required(func):  # 自定义登录验证装饰器
    def warpper(request, *args, **kwargs):
        timenow = datetime.datetime.now()
        T_Now = timenow.minute + timenow.hour * 60
        config.read("web.ini",encoding='utf-8')

        name = request.GET.get('name', default='e')
        if name == 'e':
            return HttpResponseRedirect("/") #没有名字，直接跳转登录页
        else:
            try:
                T_logout = int(config.get(name,'T_current')) #名字正确继续执行
                interval = int(T_Now - T_logout)
                if interval>1000:
                    config.set(name,'is_login','false')
                else:
                    config.set(name, 'T_current',str(T_Now))
                config.write(open("web.ini", "w",encoding='utf-8'))
            except:
                return HttpResponseRedirect("/")
        is_login = config.get(name,'is_login')

        if is_login == 'true':
            return func(request, *args, **kwargs)
        else:

            return HttpResponseRedirect("/")
    return warpper

@login_required
def main(request):

    if request.method == 'POST':
        pass


    else:
        config.read("web.ini",encoding='utf-8')

        i = 0
        channel = ['未知']*64
        while i < 64:
            channel[i] =  config.get("configinfo", "channel" + str(i+1))
            i = i + 1
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        audiotype = config.get("configinfo", "audiotype")
        print(audiotype)
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        with open(file=file_path, mode="a", encoding="utf-8") as f:
            f.write(f'{time} {name}登录\n')

        return render(request, 'system/main.html',{'name':name,'permiss':permiss,'channels':channel,'r_status':r_status,'type':audiotype})

def btn_action(request):
    data = request.POST['mes']
    print(data)
    mark = send_data(data)
    if mark == False:
        return JsonResponse({'msg': 'failed'})
    else:
        return JsonResponse({'msg': 'success'})


def get_diskstatus(request):
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p('C:/'), None, None, ctypes.pointer(free_bytes))
    no = round(free_bytes.value / 1024 / 1024 / 1024,2)

    return JsonResponse({'no': no, 'msg': 'success'})#pcm 一个通道：采样率*2*s B  mp3 目标比特率*s bite

def get_val(request):

    no = request.POST['no']

    datadict = {'MSG_TYPE': 'GETCHANNELDB', 'CHANNELINDEX':no}
    data = json.dumps(datadict)
    rest = send_data(data)
    if rest == False:
        return JsonResponse({'msg': 'error'})
    else:
        return JsonResponse({'msg': 'OK','val': rest})

def record_status(request):
    if request.method == 'POST':
        no = int(request.POST['no'])-1
        act = request.POST['act']
        if no ==99:
            for i in range(64):
                r_status[i] = act
        else:
            r_status[no] = act
    else:
        pass
    return JsonResponse({'msg': 'success'})

@login_required
def system_config(request):
    config.read("web.ini",encoding='utf-8')
    i = 0
    channelname = ['未知'] * 64
    audiomode = ['未知'] * 64
    channel = ['未知'] * 64
    while i < 64:
        channelname[i] = config.get("configinfo", "channel" + str(i + 1))
        audiomode[i] = config.get("configinfo", "audiomode" + str(i + 1))
        channel[i] = [channelname[i],audiomode[i]]
        i = i + 1
    if request.method == 'POST':
        form = SysconfigForm(request.POST)
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        if form.is_valid():

            u_name = form.cleaned_data['usrname_n']
            u_permiss = form.cleaned_data['usr_perssions_n']

            audiotype = form.cleaned_data['audiotype']
            filepath = form.cleaned_data['path']
            filepath = filepath.replace('\\', '/')
            infolist = {'mp3':'1','wav':'0','全时段录音':'1','自动录音':'0'}

            datadict = {'MSG_TYPE':'RECORDCONFIG','FORMAT':infolist[audiotype],'LOCATION':filepath}
            data = json.dumps(datadict)
            rest = send_data(data)
            if rest == False:
                return render(request, 'system/sysconfig.html', {'form': form,'name':u_name,'permiss':u_permiss,'res':'failed'})

            raudiotype = config.get("configinfo", "audiotype")
            config.set("configinfo", "audiotype", audiotype)
            config.set("configinfo", "filepath", filepath)
            with open(file=file_path, mode="a", encoding="utf-8") as f:
                f.write(f'{time} {u_name}用户 将存储格式:{raudiotype}修改为存储格式{audiotype}\n')

            config.write(open("web.ini","w",encoding='utf-8'))

            return render(request, 'system/sysconfig.html', {'form': form,'name':u_name,'permiss':u_permiss})
        else:

            return render(request, 'system/sysconfig.html', {'form': form})


    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        form = SysconfigForm()
        audiotype = config.get("configinfo","audiotype")
        filepath = config.get("configinfo", "filepath")

        if permiss == '管理员':
            return render(request, 'system/sysconfig.html',{'form': form,'method':'get','name':name,'permiss':permiss,'audiotype':audiotype,'filepath':filepath,
                                                        'channels':channel})
        else:
            return render(request, 'system/error.html',{'name':name,'permiss':permiss,'ecode':0})

@login_required
def channel_config(request):
    if request.method == 'POST':
        form = ChannelForm(request.POST)
        if form.is_valid():

                name = form.cleaned_data['usrname_n']
                permiss = form.cleaned_data['usr_perssions_n']

                no = form.cleaned_data['channelNo']

                audiomode = form.cleaned_data['audiomode']
                channelname = form.cleaned_data['channelname']
                recordval = form.cleaned_data['recordval']
                mutetime = form.cleaned_data['mutetime']

                infolist = {'全时段录音': '1', '自动录音': '0'}

                datadict = {"MSG_TYPE": "RECORDCONFIGONE", "CHANNELINFO":{"CHANNELINDEX":no,"CHANNELNAME":"ch"+no,"MOD":infolist[audiomode],"PCMDB":mutetime,"PCMPERIOD":recordval} }
                data = json.dumps(datadict)
                rest = send_data(data)
                if rest == False:
                    return render(request, 'system/channelconfig.html',
                                  {'form': form, 'name': name, 'permiss': permiss, 'res': 'failed'})



                config.set("configinfo", "audiomode"+no, audiomode)
                config.set("configinfo", "channel" + no, channelname)
                config.set("configinfo", "recordval" + no, recordval)
                config.set("configinfo", "mutetime" + no, mutetime)

                config.write(open("web.ini", "w", encoding='utf-8'))

                return HttpResponseRedirect('/system/sysconfig.html?name=' + name + '&permiss=' + permiss)

        else:
            return render(request, 'system/channelconfig.html', {'form': form})
    else:
        form = ChannelForm()
        no = request.GET.get('no')
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')

        audiomode = config.get("configinfo", "audiomode"+no)
        channelname = config.get("configinfo", "channel"+no)
        recordval = config.get("configinfo", "recordval"+no)
        mutetime = config.get("configinfo", "mutetime"+no)
        return render(request, 'system/channelconfig.html', {'form': form,'name': name, 'permiss': permiss,
                                                             'channelno':no,'audiomode':audiomode,'channelname':channelname,
                                                             'recordval':recordval,'mutetime':mutetime,'method':'get'})

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
            config.read("web.ini",encoding='utf-8')
            dev = config.get("systeminfo", "netdev")
            pw = config.get("systeminfo", "syspw")
            path0 = config.get("systeminfo", "path")
            path = path0+ dev
            sudoCMD('chmod 777 '+ path,pw)
            sudoCMD('touch ' + path+'cp', pw)
            sudoCMD('chmod 777 ' + path+'cp', pw)
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
            sudoCMD('reboot', pw)
        return render(request, 'system/netconfig.html')
    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        form = NetForm()
        return render(request, 'system/netconfig.html', {'name': name, 'permiss': permiss, 'form': form})

@login_required
def usr_config(request):
    if request.method == 'POST':
        pass

    else:
        config.read("web.ini",encoding='utf-8')
        usrinfo = config.items('usrinfo')

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

            config.read("web.ini",encoding='utf-8')
            try:
                config.add_section(name)
                config.set(name, "name", name)
                config.set(name, "pw", pw.hexdigest())
                config.set("usrinfo", name, perssions)
                config.write(open("web.ini", "w",encoding='utf-8'))

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



        config.read("web.ini",encoding='utf-8')
        config.remove_section(usrname)
        config.remove_option("usrinfo",usrname)

        config.write(open("web.ini", "w",encoding='utf-8'))

        return HttpResponseRedirect('/system/usrconfig.html?name='+name+'&permiss='+permiss)


def remote_control(request):
    if request.method == 'POST':
        config.read("web.ini",encoding='utf-8')
        pw = config.get("systeminfo", "syspw")
        method = request.POST.get('mark')
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
    config.read("web.ini",encoding='utf-8')
    path_conf = config.get("configinfo", "filepath")
    chan_list=[]
    num =1
    while num<65:
        channel = config.get("configinfo", "channel"+str(num))
        chan_list.append(channel)
        num = num+1


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
            path0 = path_conf + start_date
            if not os.path.exists(path0):
                pass
            else:

                i = 1

                while i < 65:
                    path = path_conf + start_date + '/ch' + str(i)
                    if not os.path.exists(path):
                        pass

                    else:
                        mark = False
                        F_lists = []
                        Flists = os.listdir(path)
                        for Flist in Flists:
                            Flist1 = re.sub('.mp3','',Flist)
                            Flist0 = re.sub('.wav', '', Flist1)
                            Flist2 = re.sub('-', '', Flist0)



                            if start_date == end_date:
                                if (int(start_time)-int(Flist2))<=0 and (int(end_time)-int(Flist2))>=0:
                                    F_lists.append(Flist)
                                    f_lists[start_date + '/ch' + str(i)] = F_lists
                                    mark = True
                            else:

                                if (int(start_time)-int(Flist2))<=0:
                                    F_lists.append(Flist)
                                    f_lists[start_date + '/ch' + str(i)] = F_lists
                                    mark = True
                        if mark == True:
                            lists.append(start_date + '/ch' + str(i))

                    i = i + 1

        else:
            path0 = path_conf + start_date
            if not os.path.exists(path0):
                pass
            else:
                path = path_conf + start_date + '/ch' + channel_no
                if not os.path.exists(path):
                    pass


                else:

                    F_lists = []
                    Flists = os.listdir(path)
                    for Flist in Flists:
                        Flist1 = re.sub('.mp3', '', Flist)
                        Flist0 = re.sub('.wav', '', Flist1)
                        Flist2 = re.sub('-', '', Flist0)


                        if (int(start_time) - int(Flist2)) <= 0:
                            F_lists.append(Flist)
                            f_lists[start_date + '/ch' + channel_no] = F_lists
                    lists.append(start_date + '/ch' + channel_no)


#处理既不是start_date也不是end_date的中间日期
        datestart = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        dateend = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        if dateend > datestart + datetime.timedelta(days=1):

            while datestart < (dateend + datetime.timedelta(days=-1)):
                datestart += datetime.timedelta(days=1)
                startdate = datetime.datetime.strftime(datestart, '%Y-%m-%d')
                if channel_no == 'all':
                    path0 = path_conf + startdate
                    if not os.path.exists(path0):
                        pass
                    else:
                        i = 1

                        while i < 65:
                            path = path_conf + startdate + '/ch' + str(i)
                            if not os.path.exists(path):
                                pass


                            else:
                                lists.append(startdate + '/ch' + str(i))

                            i = i + 1


                else:
                    path0 = path_conf + startdate
                    if not os.path.exists(path0):
                        pass
                    else:
                        path = path_conf + startdate + '/ch' + channel_no
                        if not os.path.exists(path):
                            pass

                        else:
                            lists.append(startdate + '/ch' + channel_no)

#处理end_data
        datestart = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        dateend = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        if dateend >= datestart + datetime.timedelta(days=1):
            if channel_no == 'all':
                path0 = path_conf + end_date
                if not os.path.exists(path0):
                    pass
                else:

                    i = 1

                    while i < 65:
                        path = path_conf + end_date + '/ch' + str(i)
                        if not os.path.exists(path):
                            pass

                        else:
                            mark = False
                            F_lists = []
                            Flists = os.listdir(path)
                            for Flist in Flists:
                                Flist1 = re.sub('.mp3', '', Flist)
                                Flist0 = re.sub('.wav', '', Flist1)
                                Flist2 = re.sub('-', '', Flist0)

                                if (int(end_time) - int(Flist2)) >= 0:
                                    F_lists.append(Flist)
                                    f_lists[end_date + '/ch' + str(i)] = F_lists
                                    mark = True
                            if mark == True:
                                lists.append(end_date + '/ch' + str(i))

                        i = i + 1

            else:
                path0 = path_conf + end_date
                if not os.path.exists(path0):
                    pass
                else:
                    path = path_conf + end_date + '/ch' + channel_no
                    if not os.path.exists(path):
                        pass


                    else:

                        F_lists = []
                        Flists = os.listdir(path)
                        for Flist in Flists:
                            Flist1 = re.sub('.mp3', '', Flist)
                            Flist0 = re.sub('.wav', '', Flist1)
                            Flist2 = re.sub('-', '', Flist0)


                            if (int(end_time) - int(Flist2)) >= 0:
                                F_lists.append(Flist)
                                f_lists[end_date + '/ch' + channel_no] = F_lists
                        lists.append(end_date + '/ch' + channel_no)





        return render(request, 'system/searchmid.html',
                      {'name':name,'permiss':permiss,'lists': lists, 'start_a': start, 'end_a': end, 'channel_no_a': channel_no,'mark':'post','start_data':start_date,'end_data':end_date,'chanlist':chan_list})

    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        return render(request, 'system/searchmid.html',{'name':name,'permiss':permiss,'chanlist':chan_list})

@login_required
def audio_file(request):
    if request.method == 'POST':
        pass

    else:
        config.read("web.ini", encoding='utf-8')
        path_conf = config.get("configinfo", "filepath")


        dir = request.GET.get('dir', default='10000000')
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        try:


            lists = f_lists[dir]
        except:
            path = path_conf + dir
            lists =  os.listdir(path)
        return render(request, 'system/audiofile.html', {'lists': lists, 'path': dir,'name':name,'permiss':permiss})


def send_data(data):

    try:
        r = requests.post("http://10.25.16.158:8090", data=data)
        res = r.json()
        print(res)
    except Exception as e:
        print(e)
        return False
    if res['ret_code']=='200':
        return res['ret_msg']
    else:
        return False





def heartbeat(request):
    # res = udp.heartbeat()
    # if res==0:
    #     return JsonResponse({'msg': 'failed'})

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
            name = request.POST.get('usrname_n', default='10000000')
            permiss = request.POST.get('usr_perssions_n', default='10000000')
            page_num = request.POST.get('page', 1)
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

        return render(request,'system/free.html',locals(),{'name':name,'permiss':permiss})



def devices(request):
    if request.method =="POST":
        pass
    else:
        config.read("web.ini",encoding='utf-8')

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

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
from .forms import SysconfigForm, UsrForm, NetForm, ChannelForm, UsreditForm
import os, hashlib, json, re
import time, datetime, configparser, requests
import ctypes
import psutil

time.time()
now = datetime.datetime.now()
timestr = now.strftime("%Y-%m-%d")

dir = os.getcwd() + '/logs'
if not os.path.exists(dir):
    os.mkdir(dir)
file_path = dir + '/' + timestr + '.txt'
print(file_path)

f_lists = {}
config = configparser.ConfigParser()
config1 = configparser.ConfigParser()

r_status = ['off'] * 32

def sudoCMD(command, password):
    str = os.system('echo %s | sudo -S %s' % (password, command))
    print(str)

def checkstatus():
    for status in r_status:
        if status == 'on':
            return False
    return True

def login_required(func):  # 自定义登录验证装饰器
    def warpper(request, *args, **kwargs):
        timenow = datetime.datetime.now()
        T_Now = timenow.minute * 60 + timenow.hour * 60 * 60 + timenow.second
        config1.read("admin.ini", encoding='utf-8-sig')
        name = request.GET.get('name', default='e')
        if name == 'e':
            return HttpResponseRedirect("/")  # 没有名字，直接跳转登录页
        else:
            try:
                T_logout = int(config1.get(name, 't_current'))  # 名字正确继续执行
                interval = int(T_Now - T_logout)
                if interval > 6:
                    config1.set(name, 'is_login', 'false')
                else:
                    config1.set(name, 't_current', str(T_Now))
                config1.write(open("admin.ini", "w", encoding='utf-8-sig'))
            except:
                return HttpResponseRedirect("/")
        is_login = config1.get(name, 'is_login')
        if is_login == 'true':
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect("/")
    return warpper

#@login_required
def main(request):
    if request.method == 'POST':
        pass


    else:
        config.read("web.ini", encoding='utf-8-sig')

        i = 0
        channel = ['未知'] * 32
        while i < 32:
            channel[i] = config.get("configinfo", "channel" + str(i + 1))
            i = i + 1
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        audiotype = config.get("configinfo", "audiotype")
        diskwarn = config.get("configinfo", "diskwarn")

        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        with open(file=file_path, mode="a", encoding="utf-8-sig") as f:
            f.write(f'{time} {name}登录\n')

        return render(request, 'system/main.html',
                      {'name': name, 'permiss': permiss, 'channels': channel, 'r_status': r_status, 'type': audiotype,
                       'diskwarn': diskwarn})

def btn_action(request):
    data = request.POST['mes']
    print(data)
    mark = send_data(data)
    if mark == False:
        return JsonResponse({'msg': 'failed'})
    else:
        return JsonResponse({'msg': 'success'})

def get_diskstatus(request):
    config.read("web.ini", encoding='utf-8-sig')
    diskspace = config.get("configinfo", "diskspace")
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(diskspace), None, None, ctypes.pointer(free_bytes))
    no = round(free_bytes.value / 1024 / 1024 / 1024, 2)

    return JsonResponse({'no': no, 'msg': 'success'})  # pcm 一个通道：采样率*2*s B  mp3 目标比特率*s bite

def get_serverstatus(request):
    server_info = {}
    cpu_percent = psutil.cpu_percent(interval=1)
    server_info["cpu_usage"] = "%i%%" % cpu_percent

    virtual_memory = psutil.virtual_memory()
    used_memory = virtual_memory.used / 1024 / 1024 / 1024
    free_memory = virtual_memory.free / 1024 / 1024 / 1024
    server_info["mem_usage"] = "%0.2fG/%0.2fG" % (used_memory, used_memory + free_memory);

    return JsonResponse({'serverInfo': server_info, 'msg': 'success'})

def get_val(request):
    no = request.POST['no']

    datadict = {'MSG_TYPE': 'GETCHANNELDB', 'CHANNELINDEX': no}
    data = json.dumps(datadict)
    rest = send_data(data)
    if rest == False:
        return JsonResponse({'msg': 'error'})
    else:
        return JsonResponse({'msg': 'OK', 'val': rest})

def record_status(request):
    if request.method == 'POST':
        no = int(request.POST['no']) - 1
        act = request.POST['act']
        if no == 99:
            for i in range(32):
                r_status[i] = act
        else:
            r_status[no] = act
    else:
        pass
    return JsonResponse({'msg': 'success'})

#@login_required
def system_config(request):
    config.read("web.ini", encoding='utf-8-sig')
    i = 0
    channelname = ['未知'] * 32
    audiomode = ['未知'] * 32
    save = ['未知'] * 32
    channel = ['未知'] * 32
    while i < 32:
        index = i+1
        channelname[i] = config.get("configinfo", "n_channel" + str(index))
        audiomode[i] = config.get("configinfo", "n_audiomode" + str(index))
        save[i] = config.get("configinfo", "status" + str(index))
        channel[i] = [channelname[i], audiomode[i], save[i]]
        i = i + 1
    if request.method == 'POST':
        form = SysconfigForm(request.POST)
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        if form.is_valid():
            infolist = {'mp3': '0', 'wav': '1', '全时段录音': '1', '自动录音': '0'}
            u_name = form.cleaned_data['usrname_n']
            u_permiss = form.cleaned_data['usr_perssions_n']
            # 检查设备在线状态
            val = checkstatus()
            if val:
                pass
            else:
                return render(request, 'system/sysconfig.html',
                              {'form': form, 'name': u_name, 'permiss': u_permiss, 'res': 'online',
                               'channels': channel})
            audiotype = form.cleaned_data['audiotype']
            audiotime0 = form.cleaned_data['audiotime']
            audiotime1 = int(audiotime0) * 60
            audiotime = str(audiotime1)
            all_info = []
            for i in range(1, 33):
                no = str(i)
                if config.get("configinfo", "status" + no) == "false":
                    channel_info = {}
                    channel_info["CHANNELINDEX"] = no
                    channel_info["CHANNELNAME"] = config.get("configinfo", "n_channel" + no)
                    channel_info["MOD"] = infolist.get(config.get("configinfo", "n_audiomode" + no))
                    channel_info["PCMDB"] = config.get("configinfo", "n_recordval" + no)
                    channel_info["PCMPERIOD"] = config.get("configinfo", "n_mutetime" + no)
                    channel_info["MAINCOMMENT"] = config.get("configinfo", "n_main_comment" + no)
                    channel_info["SUBCOMMENT"] = config.get("configinfo", "n_sub_comment" + no)
                    all_info.append(channel_info)
            datadict = {'MSG_TYPE': 'RECORDCONFIGALL', 'FORMAT': infolist[audiotype], 'PERIOD': audiotime,
                        "CHANNELS": all_info}
            data = json.dumps(datadict)
            rest = send_data(data)
            if rest == False:
                return render(request, 'system/sysconfig.html',
                              {'form': form, 'name': u_name, 'permiss': u_permiss, 'res': 'failed',
                               'channels': channel})
            else:
                raudiotype = config.get("configinfo", "audiotype")
                config.set("configinfo", "audiotype", audiotype)
                config.set("configinfo", "audiotime", audiotime0)
                for info in all_info:
                    no = info["CHANNELINDEX"]
                    config.set("configinfo", "channel" + no, info["CHANNELNAME"])
                    config.set("configinfo", "recordval" + no, info["PCMDB"])
                    config.set("configinfo", "mutetime" + no, info["PCMPERIOD"])
                    if info["MOD"]>0:
                        config.set("configinfo", "audiomode" + no, "全时段录音")
                    else:
                        config.set("configinfo", "audiomode" + no, "自动录音")
                    config.set("configinfo", "main_comment" + no, info["MAINCOMMENT"])
                    config.set("configinfo", "sub_comment" + no, info["SUBCOMMENT"])
                    config.set("configinfo", "status" + no, 'true')
                config.write(open("web.ini", "w", encoding='utf-8-sig'))
                with open(file=file_path, mode="a", encoding="utf-8-sig") as f:
                    f.write(f'{time} {u_name}用户 将存储格式:{raudiotype}修改为存储格式{audiotype}\n')
            return render(request, 'system/sysconfig.html',
                          {'form': form, 'name': u_name, 'permiss': u_permiss, 'channels': channel})
        else:
            return render(request, 'system/sysconfig.html', {'form': form})
    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        form = SysconfigForm()
        audiotype = config.get("configinfo", "audiotype")
        audiotime = config.get("configinfo", "audiotime")
        if permiss == '管理员':
            return render(request, 'system/sysconfig.html',
                          {'form': form, 'method': 'get', 'name': name, 'permiss': permiss, 'audiotype': audiotype,
                           'audiotime': audiotime, 'channels': channel})
        else:
            return render(request, 'system/error.html', {'name': name, 'permiss': permiss, 'ecode': 0})

#@login_required
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
            main_comment = form.cleaned_data['main_comment']
            sub_comment = form.cleaned_data['sub_comment']

            saveconfig = form.cleaned_data['saveconfig']
            goback = form.cleaned_data['goback']

            config.read("web.ini", encoding='utf-8-sig')
            audiomode_c = config.get("configinfo", "audiomode" + no)
            channelname_c = config.get("configinfo", "channel" + no)
            recordval_c = config.get("configinfo", "recordval" + no)
            mutetime_c = config.get("configinfo", "mutetime" + no)
            main_comment_c = config.get("configinfo", "main_comment" + no)
            sub_comment_c = config.get("configinfo", "sub_comment" + no)

            if goback == 'true':  # 返回跳转处
                return HttpResponseRedirect('/system/sysconfig.html?name=' + name + '&permiss=' + permiss)
            if (audiomode == audiomode_c) & (channelname == channelname_c) & (recordval == recordval_c) & (
                    mutetime == mutetime_c) & (main_comment == main_comment_c) & (sub_comment == sub_comment_c):
                return render(request, 'system/channelconfig.html',
                              {'form': form, 'name': name, 'permiss': permiss, 'res': 'same'})
            if checkstatus():  # 检查所有通道是否关闭
                pass
            else:
                return render(request, 'system/channelconfig.html',
                              {'form': form, 'name': name, 'permiss': permiss, 'res': 'online'})
            if saveconfig == 'false':  # 保存配置跳转处
                config.set("configinfo", "n_audiomode" + no, audiomode)
                config.set("configinfo", "n_channel" + no, channelname)
                config.set("configinfo", "n_recordval" + no, recordval)
                config.set("configinfo", "n_mutetime" + no, mutetime)
                config.set("configinfo", "n_main_comment" + no, main_comment)
                config.set("configinfo", "n_sub_comment" + no, sub_comment)
                config.set("configinfo", "status" + no, 'false')
                config.write(open("web.ini", "w", encoding='utf-8-sig'))
                return HttpResponseRedirect('/system/sysconfig.html?name=' + name + '&permiss=' + permiss)
        else:
            return render(request, 'system/channelconfig.html', {'form': form})
    else:
        config.read("web.ini", encoding='utf-8-sig')
        form = ChannelForm()
        no = request.GET.get('no')
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        reset = request.GET.get('reset', default='10000000')

        if reset == 'true':  # 还原配置跳转处
            audiomode = config.get("configinfo", "audiomode" + no)
            channelname = config.get("configinfo", "channel" + no)
            recordval = config.get("configinfo", "recordval" + no)
            mutetime = config.get("configinfo", "mutetime" + no)
            main_comment = config.get("configinfo", "main_comment" + no)
            sub_comment = config.get("configinfo", "sub_comment" + no)

            config.set("configinfo", "n_audiomode" + no, '')
            config.set("configinfo", "n_channel" + no, '')
            config.set("configinfo", "n_recordval" + no, '')
            config.set("configinfo", "n_mutetime" + no, '')
            config.set("configinfo", "n_main_comment" + no, '')
            config.set("configinfo", "n_sub_comment" + no, '')
            config.set("configinfo", "status" + no, 'true')

            config.write(open("web.ini", "w", encoding='utf-8-sig'))
            return render(request, 'system/channelconfig.html', {'form': form, 'name': name, 'permiss': permiss,
                                                                 'channelno': no, 'audiomode': audiomode,
                                                                 'channelname': channelname,
                                                                 'recordval': recordval, 'mutetime': mutetime,
                                                                 'main_comment': main_comment,
                                                                 'sub_comment': sub_comment,
                                                                 'method': 'get', 'save': 'true'})
        else:
            status = config.get("configinfo", "status" + no)

            if status == 'false':
                audiomode = config.get("configinfo", "n_audiomode" + no)
                channelname = config.get("configinfo", "n_channel" + no)
                recordval = config.get("configinfo", "n_recordval" + no)
                mutetime = config.get("configinfo", "n_mutetime" + no)
                main_comment = config.get("configinfo", "n_main_comment" + no)
                sub_comment = config.get("configinfo", "n_sub_comment" + no)
            else:
                audiomode = config.get("configinfo", "audiomode" + no)
                channelname = config.get("configinfo", "channel" + no)
                recordval = config.get("configinfo", "recordval" + no)
                mutetime = config.get("configinfo", "mutetime" + no)
                main_comment = config.get("configinfo", "main_comment" + no)
                sub_comment = config.get("configinfo", "sub_comment" + no)
            return render(request, 'system/channelconfig.html', {'form': form, 'name': name, 'permiss': permiss,
                                                                 'channelno': no, 'audiomode': audiomode,
                                                                 'channelname': channelname,
                                                                 'recordval': recordval, 'mutetime': mutetime,
                                                                 'main_comment': main_comment,
                                                                 'sub_comment': sub_comment, 'method': 'get',
                                                                 'save': status})

#@login_required
def net_config(request):
    if request.method == 'POST':
        form = NetForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['usrname_n']
            permiss = form.cleaned_data['usr_perssions_n']
            ip = form.cleaned_data['ip']
            mask = form.cleaned_data['mask']
            gateway = form.cleaned_data['netgate']
            config.read("web.ini", encoding='utf-8-sig')
            dev = config.get("systeminfo", "netdev")
            pw = config.get("systeminfo", "syspw")
            path0 = config.get("systeminfo", "path")
            path = path0 + dev
            sudoCMD('chmod 777 ' + path, pw)
            sudoCMD('touch ' + path + 'cp', pw)
            sudoCMD('chmod 777 ' + path + 'cp', pw)
            with open(path + 'cp', mode='w', encoding='utf-8-sig') as fw, open(path, mode='r',
                                                                               encoding='utf-8-sig') as fr:
                for line in fr:
                    if 'BOOTPROTO' in line:
                        line = 'BOOTPROTO=static\n'
                    elif 'ONBOOT' in line:
                        line = 'ONBOOT=yes\n'
                    elif 'GATEWAY' in line:
                        line = 'GATEWAY=' + gateway + '\n'
                    elif 'IPADDR' in line:
                        line = 'IPADDR=' + ip + '\n'
                    elif 'NETMASK' in line:
                        line = 'NETMASK=' + mask + '\n'
                    fw.write(line)
            fr.close()
            fw.close()
            with open(path + 'cp', mode='r', encoding='utf-8-sig') as fr1, open(path, mode='w',
                                                                                encoding='utf-8-sig') as fw1:
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

#@login_required
def usr_config(request):
    if request.method == 'POST':
        pass

    else:
        config1.read("admin.ini", encoding='utf-8-sig')
        usrinfo = config1.items('usrinfo')

        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        if permiss == '管理员':

            return render(request, 'system/usrconfig.html', {'name': name, 'permiss': permiss, 'usrinfo': usrinfo})
        else:
            return render(request, 'system/error.html', {'name': name, 'permiss': permiss, 'ecode': 0})

#@login_required
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

            config1.read("admin.ini", encoding='utf-8-sig')
            try:
                config1.add_section(name)
                config1.set(name, "name", name)
                config1.set(name, "pw", pw.hexdigest())
                config1.set("usrinfo", name, perssions)
                config1.write(open("admin.ini", "w", encoding='utf-8-sig'))

                now = datetime.datetime.now()
                time = now.strftime("%Y-%m-%d %H:%M:%S")
                with open(file=file_path, mode="a", encoding="utf-8-sig") as f:
                    f.write(f'{time} {u_name}用户 新建用户{name}权限:{perssions}\n')
                return HttpResponseRedirect('/system/usrconfig.html?name=' + u_name + '&permiss=' + u_permiss)

            except:
                return render(request, 'system/error.html', {'name': u_name, 'permiss': u_permiss, 'ecode': 1})




    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        form = UsrForm()
        if permiss == '管理员':

            return render(request, 'system/newusr.html', {'form': form, 'name': name, 'permiss': permiss})
        else:
            return render(request, 'system/error.html', {'name': name, 'permiss': permiss, 'ecode': 0})

#@login_required
def del_usr(request):
    name = request.GET.get('name', default='10000000')
    permiss = request.GET.get('permiss', default='10000000')
    usrname = request.GET.get('usrname')
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(file=file_path, mode="a", encoding="utf-8-sig") as f:
        f.write(f'{time} {name}用户 删除用户{usrname}权限:{permiss}\n')

    config1.read("admin.ini", encoding='utf-8-sig')
    config1.remove_section(usrname)
    config1.remove_option("usrinfo", usrname)

    config.write(open("admin.ini", "w", encoding='utf-8-sig'))

    return JsonResponse({'msg': 'success'})

def remote_control(request):
    if request.method == 'POST':
        config.read("web.ini", encoding='utf-8-sig')
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

#@login_required
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

            config1.read("admin.ini", encoding='utf-8-sig')

            pw_conf = config1.get(name, "pw")
            if pw.hexdigest() == pw_conf:
                m1 = n_password + "{{sdtzzq}}"
                pw1 = hashlib.md5(m1.encode())
                config1.set(name, "pw", pw1.hexdigest())

                config1.write(open("admin.ini", "w", encoding='utf-8-sig'))

                now = datetime.datetime.now()
                time = now.strftime("%Y-%m-%d %H:%M:%S")
                # with open(file=file_path, mode="a", encoding="utf-8") as f:
                #     f.write(f'{time} {u_name}用户 新建用户{name}权限:{perssions}\n')
                return HttpResponseRedirect('/system/usrconfig.html?name=' + u_name + '&permiss=' + u_permiss)
            else:
                return render(request, 'system/usredit.html',
                              {'form': form, 'name': u_name, 'permiss': u_permiss, 'method': 'error'})

    else:
        form = UsreditForm()
        usrname = request.GET.get('usrname')
        usrpermiss = request.GET.get('usrpermiss')
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        if permiss == '管理员':

            return render(request, 'system/usredit.html',
                          {'name': name, 'permiss': permiss, 'form': form, 'usrname': usrname, 'usrpermiss': usrpermiss,
                           'method': 'get'})
        else:
            return render(request, 'system/error.html', {'name': name, 'permiss': permiss, 'ecode': 0})

#@login_required
def search_mid_bak(request):
    config.read("web.ini",encoding='utf-8-sig')

    chan_list=[]
    num =1
    while num<33:
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
            path0 = 'static/record/' + start_date
            if not os.path.exists(path0):
                pass
            else:

                i = 1

                while i < 33:
                    path = 'static/record/' + start_date + '/ch' + str(i)
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
                            Flist2 = Flist2[-6:]




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
            path0 = 'static/record/' + start_date
            if not os.path.exists(path0):
                pass
            else:
                path = 'static/record/' + start_date + '/ch' + channel_no
                if not os.path.exists(path):
                    pass


                else:

                    F_lists = []
                    Flists = os.listdir(path)
                    for Flist in Flists:
                        Flist1 = re.sub('.mp3', '', Flist)
                        Flist0 = re.sub('.wav', '', Flist1)
                        Flist2 = re.sub('-', '', Flist0)
                        Flist2 = Flist2[-6:]


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
                    path0 = 'static/record/' + startdate
                    if not os.path.exists(path0):
                        pass
                    else:
                        i = 1

                        while i < 33:
                            path = 'static/record/' + startdate + '/ch' + str(i)
                            if not os.path.exists(path):
                                pass


                            else:
                                lists.append(startdate + '/ch' + str(i))

                            i = i + 1


                else:
                    path0 = 'static/record/' + startdate
                    if not os.path.exists(path0):
                        pass
                    else:
                        path = 'static/record/' + startdate + '/ch' + channel_no
                        if not os.path.exists(path):
                            pass

                        else:
                            lists.append(startdate + '/ch' + channel_no)

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

                    while i < 33:
                        path = 'static/record/' + end_date + '/ch' + str(i)
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
                                Flist2 = Flist2[-6:]

                                if (int(end_time) - int(Flist2)) >= 0:
                                    F_lists.append(Flist)
                                    f_lists[end_date + '/ch' + str(i)] = F_lists
                                    mark = True
                            if mark == True:
                                lists.append(end_date + '/ch' + str(i))

                        i = i + 1

            else:
                path0 = 'static/record/' + end_date
                if not os.path.exists(path0):
                    pass
                else:
                    path = 'static/record/' + end_date + '/ch' + channel_no
                    if not os.path.exists(path):
                        pass


                    else:

                        F_lists = []
                        Flists = os.listdir(path)
                        for Flist in Flists:
                            Flist1 = re.sub('.mp3', '', Flist)
                            Flist0 = re.sub('.wav', '', Flist1)
                            Flist2 = re.sub('-', '', Flist0)
                            Flist2 = Flist2[-6:]


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

#@login_required
def search_mid(request):
    config.read("web.ini", encoding='utf-8-sig')
    # 获取备选列表
    chan_list = []
    for num in range(1, 33):
        channel_name = config.get("configinfo", "channel" + str(num))
        chan_list.append(channel_name)
    if request.method == 'POST':
        root_path = 'static/record/'    #录音存储路径
        return_list = []
        channel_list = []               #选中的通道
        date_list = []                  #选中的日期
        # 参数获取
        name = request.POST['usrname_n']
        permiss = request.POST['usr_perssions_n']
        main_comment = request.POST['main_comment']
        #sub_comment = request.POST['sub_comment']
        sub_comment = ""    #配合前端备注二不显示，这里默认为""
        start = request.POST['start']
        start_time = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M')
        start_date = start_time.strftime('%Y-%m-%d')
        end = request.POST['end']
        end_time = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M')
        end_date = end_time.strftime('%Y-%m-%d')
        date_list = getDataList(start_date, end_date)
        for key in request.POST:
            if key.find("ch") > -1:
                channel_list.append(key)
        for date in date_list:
            if not os.path.exists(root_path + date):
                pass
            else:
                if len(channel_list) < 1:
                    pass
                for ch in channel_list:
                    if not os.path.exists(root_path + date + "/" + ch):
                        pass
                    else:
                        file_list = os.listdir(root_path + date + "/" + ch)
                        for file_name in file_list:
                            if (main_comment != "") & (file_name.find(main_comment) < 0):
                                pass
                            else:
                                if (sub_comment != "") & (file_name.find(sub_comment) < 0):
                                    pass
                                else:
                                    temp = file_name.split("_")[2].split("T")[1].replace("-", ":")
                                    serch_time = file_name.split("_")[2].split("T")[0] + "T" + temp
                                    serch_time = datetime.datetime.strptime(serch_time, '%Y-%m-%dT%H:%M:%S')
                                    if start_time <= serch_time <= end_time:
                                        time = file_name.split("_")[2].split("T")[1]
                                        return_list.append(date + " " + time + " / " + file_name)
        return render(request, 'system/searchmid.html',
                      {'name': name, 'permiss': permiss, 'mark': 'post', 'start_a': start, 'end_a': end, 'start_data': start_date, 'end_data': end_date,
                       'main_comment': main_comment, 'sub_comment': sub_comment, 'select_list': channel_list, 'chanlist': chan_list, 'lists': return_list})
    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        return render(request, 'system/searchmid.html', {'name': name, 'permiss': permiss, 'chanlist': chan_list})

#@login_required
def audio_file(request):
    if request.method == 'POST':
        pass
    else:
        file = request.GET.get('file')
        time = file.split("/ ")[0].split(" ")[0]
        file = file.split("/ ")[1]
        ch = file.split("_")[1]
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        path = 'static/record/' + time + "/" + ch + "/" + file
        return render(request, 'system/audiofile.html', {'path': path, 'name': name, 'permiss': permiss})

def send_data(data):
    config.read("web.ini", encoding='utf-8-sig')
    ip = config.get("systeminfo", "serverip")
    try:
        r = requests.post("http://" + ip, data=data)
        res = r.json()
        print(res)
    except Exception as e:
        print(e)
        return False
    if res['ret_code'] == '200':
        return res['ret_msg']
    else:
        return False

def heartbeat(request):
    # res = udp.heartbeat()
    # if res==0:
    #     return JsonResponse({'msg': 'failed'})
    timenow = datetime.datetime.now()
    T_Now = timenow.minute * 60 + timenow.hour * 60 * 60 + timenow.second
    name = request.GET.get('name', default='10000000')
    config1.read("admin.ini", encoding='utf-8-sig')
    config1.set(name, 't_current', str(T_Now))
    config1.write(open("admin.ini", "w", encoding='utf-8-sig'))

    return JsonResponse({'msg': 'success'})

#
# """
# 日志信息
# yxy
# 添加日志
# """
def free_logs(request):
    if request.method == 'POST':
        data = json.loads(request.POST['mes'])
        start_time = data.get('start_time')
        end_time = data.get("end_time")
        user_name = data.get("name")
        channel_no = data.get("channel_no")
        channel_name = data.get("channel_name")
        if end_time is None:
            with open(file=file_path, mode="a", encoding="utf-8-sig") as f:
                f.write(f'{start_time} 用户:{user_name}开始录音 通道号:{channel_no} 通道名:{channel_name}\n')
        else:
            with open(file=file_path, mode="a", encoding="utf-8-sig") as f:
                f.write(f'{end_time} 用户:{user_name}停止录音 通道号:{channel_no} 通道名:{channel_name}\n')
        return JsonResponse({'mes': "ok"})
    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        return render(request, 'system/free.html', {'name': name, 'permiss': permiss})

# 这个主要是返回html模板
def free_html(request):
    if request.method == "POST":
        pass
    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        return render(request, 'system/free.html', {'name': name, 'permiss': permiss})

# 这里现在是查询展示日志的功能，
def free_count(request):
    if request.method == "POST":
        pass

    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        page_num = request.GET.get('page', 1)
        st = request.GET.get('start')
        et = request.GET.get('end')
        if st is not None and et is not None:
            name = request.POST.get('usrname_n', default='10000000')
            permiss = request.POST.get('usr_perssions_n', default='10000000')
            page_num = request.POST.get('page', 1)
            listdivd = []
            listdir = os.listdir(dir)
            for i in listdir:
                time_os = i[0:10]
                if time_os >= st and time_os <= et:
                    with open(file=dir + '/' + i, mode="r", encoding="utf-8-sig") as f:
                        data = f.readlines()
                        listdivd.extend(data)

            paginator = Paginator(listdivd, 25)
            try:
                # print(page)
                book_list = paginator.page(int(page_num))  # 获取当前页码的记录
            except PageNotAnInteger:
                book_list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
            except EmptyPage:
                book_list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页`码列表中时,显示最后一页的内容

        return render(request, 'system/free.html', locals(), {'name': name, 'permiss': permiss})

def devices(request):
    if request.method == "POST":
        pass
    else:
        config.read("web.ini", encoding='utf-8-sig')

        audiotype = config.get("configinfo", "audiotype")
        channel1 = config.get("configinfo", "channel1")
        channel2 = config.get("configinfo", "channel2")
        channel3 = config.get("configinfo", "channel3")
        channel4 = config.get("configinfo", "channel4")
        listd = {"data":
                     [{"id": "1",
                       "name": channel1,
                       "status": r_status[0],
                       "fileType": audiotype
                       },
                      {"id": "2",
                       "name": channel2,
                       "status": r_status[1],
                       "fileType": audiotype},
                      {"id": "3",
                       "name": channel3,
                       "status": r_status[2],
                       "fileType": audiotype},
                      {"id": "4",
                       "name": channel4,
                       "status": r_status[3],
                       "fileType": audiotype}]}
    return JsonResponse(listd)

def getDataList(start_date, end_date):
    date_list = []
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while start_date <= end_date:
        date_str = start_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        start_date += datetime.timedelta(days=1)
    return date_list
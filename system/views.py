from django.shortcuts import render
from django.http import JsonResponse
from .forms import SysconfigForm
import os,sqlite3


# Create your views here.
def main(request):

    if request.method == 'POST':
        pass

    else:
        name = request.GET.get('name', default='10000000')
        permiss = request.GET.get('permiss', default='10000000')
        print(permiss)

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
        form = SysconfigForm()
        return render(request, 'system/sysconfig.html',{'form': form})

def usr_config(request):
    if request.method == 'POST':
        pass

    else:

        return render(request, 'system/usrconfig.html')
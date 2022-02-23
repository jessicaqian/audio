from django.shortcuts import render
from django.http import JsonResponse
import os


# Create your views here.
def main(request):

    if request.method == 'POST':
        pass

    else:
        return render(request, 'system/main.html',)

def get_diskstatus(request):
    st = os.statvfs('/home')
    status = st.f_bavail * st.f_frsize/(1024*1024*1024) #这里单位可能差了1024
    no = round(status,2)

    return JsonResponse({'no': no, 'msg': 'success'})#pcm 一个通道：采样率*2*s B  mp3 目标比特率*s bite
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import NameForm

# Create your views here.

def login(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            return HttpResponseRedirect('/system/main.html')
        else:
            return render(request, 'admin/login.html', {'form': form})
    else:
        form = NameForm()
    return render(request, 'admin/login.html', {'form': form})

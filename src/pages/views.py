from django.contrib.auth.views import login
from django.shortcuts import render, redirect


def custom_login(request, *args, **kwargs):
    if request.user.is_authenticated():
        return redirect('/', *args, **kwargs)
    else:
        return login(request, *args, **kwargs)


def index(request):
    return render(request, 'pages/index.html')


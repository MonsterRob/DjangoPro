from django.shortcuts import render, redirect
from .models import UserInfo
from django.http import JsonResponse


# Create your views here.

def login(request):
    context = {'title': '登陆'}
    return render(request, 'duser/login.html', context)


def register(request):
    context = {'title': '注册'}
    return render(request, 'duser/register.html', context)


def index(request):
    return redirect('duser:login')


def check_name(request):
    name = request.GET.get('uname')

    obj = UserInfo.objects.filter(uname=name)

    if obj:
        return JsonResponse({'result': True})
    else:
        return JsonResponse({'result': False})


def check_login(request):

    pass

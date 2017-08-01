from django.shortcuts import render, redirect
from .models import UserInfo
from django.http import JsonResponse, HttpResponse
from hashlib import md5


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
    uname = request.POST.get('username')
    user = UserInfo.objects.get(uname=uname)  # get 在这里不会为空
    upwd = request.POST.get('pwd')
    md = md5()
    md.update(upwd.encode())

    #  登陆成功 用户获得授权 登陆失败
    if user.upwd == md.hexdigest():

        return redirect('duser:login_ok')
    else:
        return redirect('duser:login')






def register_in(request):
    # 获取注册信息 创建模型对象并存储
    # user_name pwd email

    user_name = request.POST.get('user_name')
    pwd = request.POST.get('pwd')  # 需要加密
    email = request.POST.get('email')

    user_new = UserInfo()
    user_new.uname = user_name
    user_new.uemail = email

    md = md5()
    md.update(pwd.encode())
    user_new.upwd = md.hexdigest()
    user_new.save()
    return redirect('duser:login')


def login_ok(request):
    return HttpResponse('login ok')

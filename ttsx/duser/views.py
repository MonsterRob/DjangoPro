from django.shortcuts import render, redirect
from .models import UserInfo
from django.http import JsonResponse
from hashlib import md5
from datetime import datetime, timedelta


# Create your views here.
# 登陆验证装饰器
def logged(func):
    def check(requset, *args, **kwargs):
        if 'uid' in requset.session:
            return func(requset, *args, **kwargs)
        else:
            return redirect('duser:login')

    return check


# 用户 首页
def index(request):
    return redirect('duser:login')


# 登陆 页面
def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'uname': uname}
    return render(request, 'duser/login.html', context)


# 登陆/注册 用户名查询 json
def check_name(request):
    name = request.GET.get('uname')
    obj = UserInfo.objects.filter(uname=name)

    if obj:
        return JsonResponse({'result': True})
    else:
        return JsonResponse({'result': False})


# 登陆 表单验证 登陆成 导航显示改变 姓名|退出
def check_login(request):
    dic = request.POST
    uname = dic.get('username')
    user = UserInfo.objects.get(uname=uname)  # get 在这里不会为空

    name_jz = dic.get('name_jz', False)

    upwd = dic.get('pwd')
    md = md5()
    md.update(upwd.encode())

    #  登陆成功 用户获得授权 登陆失败
    if user.upwd == md.hexdigest():
        come_path = request.session.get('url_path', '/')  # 获取来时路径
        request.session['uid'] = user.id
        request.session['uname'] = user.uname
        response = redirect(come_path)

        if name_jz:
            response.set_cookie('uname', uname, expires=datetime.now() + timedelta(days=7))
        else:
            response.set_cookie('uname', '', max_age=-1)

        return response
    else:
        context = {'uname': uname, 'pwd_error': True}
        return render(request, 'duser/login.html', context)


def logout(request):
    request.session.flush()
    come_path = request.session.get('url_path', '/')
    return redirect(come_path)


# 注册 页面
def register(request):
    return render(request, 'duser/register.html')


# 注册 表单验证
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

    come_path = request.session.get('url_path', '/')
    return redirect(come_path)


# 用户中心-个人信息
@logged
def user_center_info(request):
    return render(request, 'duser/user_center_info.html')


# 用户中心-全部订单
@logged
def user_center_order(request):
    return render(request, 'duser/user_center_order.html')


# 用户中心-收货地址
@logged
def user_center_site(request):
    return render(request, 'duser/user_center_site.html')

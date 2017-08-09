from django.shortcuts import render, redirect
from .models import UserInfo, AreaInfo
from django.http import JsonResponse
from hashlib import md5
from datetime import datetime, timedelta
import json
from common.models import Goodsinfo, BuyInfo, BuyDetailInfo


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
    uid = request.session['uid']
    user = UserInfo.objects.get(pk=uid)
    browsed = request.COOKIES.get('browsed')
    goods = []
    if browsed:
        list_b = json.loads(browsed)
        goods = Goodsinfo.objects.filter(pk__in=list_b)
    context = {'goods': goods, 'user': user}

    return render(request, 'duser/user_center_info.html', context)


# 用户中心-全部订单
@logged
def user_center_order(request):
    # 需要拉取已结算订单信息和未结算订单信息
    buyers = BuyInfo.objects.all()  # 所有订单
    context = {'buyers': buyers}
    # 一个订单关联多件商品
    return render(request, 'duser/user_center_order.html', context)


# 用户中心-收货地址
@logged
def user_center_site(request):
    uid = request.session['uid']
    user = UserInfo.objects.get(pk=uid)
    context = {'user': user}
    return render(request, 'duser/user_center_site.html', context)


# 地址编辑
@logged
def parent(request):
    plist = AreaInfo.objects.filter(aParent__isnull=True)
    jsonList = []
    for area in plist:
        jsonList.append([area.id, area.atitle])

    return JsonResponse({'data': jsonList})


# 地址编辑
@logged
def sons(request):
    id_ = request.GET.get('pid')

    plist = AreaInfo.objects.filter(aParent_id=id_)

    jsonList = []
    for area in plist:
        jsonList.append([area.id, area.atitle])

    return JsonResponse(data={'data': jsonList})


# 地址编辑
@logged
def change_site(request):
    dic = request.POST
    province = dic['province']
    city = dic['city']
    county = dic['county']
    province = AreaInfo.objects.get(pk=int(province)).atitle
    county = AreaInfo.objects.get(pk=int(county)).atitle
    city = AreaInfo.objects.get(pk=int(city)).atitle
    detail = dic['detail']
    address = province + ' ' + city + ' ' + county + ' ' + detail
    recipients = dic['recipients']
    phone = dic['phone']
    uid = request.session['uid']
    user = UserInfo.objects.get(pk=uid)
    user.address = address
    user.phone = phone
    user.recipients = recipients
    user.save()
    data = {'address': address,
            'recpi': recipients,
            'ph': phone}
    return JsonResponse(data)

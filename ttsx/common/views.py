from django.shortcuts import render, get_object_or_404, redirect
from .models import TypeInfo, Goodsinfo, OrderInfo, BuyInfo, BuyDetailInfo
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from .serializer import GoodsSerializer
from rest_framework.renderers import JSONRenderer
from django.core import serializers
from rest_framework.parsers import JSONParser
import json
from haystack.generic_views import SearchView
from duser.views import logged
from duser.models import UserInfo
from datetime import datetime
from django.db import transaction


# 加入购物车-编辑购物车-去结算-提交订单
# 我的购物车展示所有加入到购物车的商品信息
# 去结算--选择部分商品结算
# 结算页-提交订单
# Create your views here.
# 全局首页
def index(request):
    types = TypeInfo.objects.all()
    list_ = []

    for typeinfo in types:
        list_.append({
            'type': typeinfo,
            'list_new': typeinfo.goodsinfo_set.order_by('-id')[0:4],
            'list_click': typeinfo.goodsinfo_set.order_by('-gclick')[0:3]
        })
    ocount = OrderInfo.objects.all().count()
    class_ = ['fruit', 'seafood', 'meet', 'egg', 'vegetables', 'ice']
    context = {'list_': list_, 'class_': class_, 'ocount': ocount}

    return render(request, 'duser/index.html', context)


# 商品详情页
def detail(request, goods_id):
    types = TypeInfo.objects.all()
    list_ = []
    for typeinfo in types:
        list_.append({
            'type': typeinfo,
        })
    class_ = ['fruit', 'seafood', 'meet', 'egg', 'vegetables', 'ice']

    goods = Goodsinfo.objects.get(pk=goods_id)
    goods.gclick += 1
    goods.save()
    new_goods = goods.gtype.goodsinfo_set.order_by('-id')[:2]
    ocount = OrderInfo.objects.all().count()
    context = {'goods': goods,
               'kucun': goods.gkucun,
               'list_': list_,
               'class_': class_,
               'new_goods': new_goods,
               'ocount': ocount}

    response = render(request, 'duser/detail.html', context)
    browsed = request.COOKIES.get('browsed')
    if browsed:
        list_b = json.loads(browsed)
        if goods_id not in list_b:
            list_b.append(goods_id)
            list_b = json.dumps(list_b)
            response.set_cookie('browsed', list_b)
    else:
        list_b = list()
        list_b.append(goods_id)
        list_b = json.dumps(list_b)
        response.set_cookie('browsed', list_b)

    return response


# 查看更多商品列表页
def more_goods(request, type_id, page_id, order_key):
    types = TypeInfo.objects.all()
    # print(serializers.serialize('json', types))

    list_ = []

    for typeinfo in types:
        list_.append({
            'type': typeinfo,
        })
    class_ = ['fruit', 'seafood', 'meet', 'egg', 'vegetables', 'ice']

    typeinfo = TypeInfo.objects.get(pk=type_id)
    orders = ['-id', 'gprice', '-gclick']

    goods_list = typeinfo.goodsinfo_set.order_by(orders[int(order_key) - 1])
    paginator = Paginator(goods_list, 5)

    page_index = int(page_id)

    if page_index <= 0:
        page_index = 1
    if page_index >= paginator.num_pages:
        page_index = paginator.num_pages

    page = paginator.page(page_index)
    prange = paginator.page_range
    if paginator.num_pages > 5:
        if page_index <= 2:
            prange = range(1, 6)

        elif page_index >= paginator.num_pages - 1:

            prange = range(paginator.num_pages - 4, paginator.num_pages + 1)
        else:
            prange = range(page_index - 2, page_index + 3)

    new_goods = typeinfo.goodsinfo_set.order_by('-id')[:2]
    pagenums = paginator.num_pages
    ocount = OrderInfo.objects.all().count()
    context = {'typeinfo': typeinfo,
               'page': page,
               'prange': prange,
               'list_': list_,
               'class_': class_,
               'order_key': order_key,
               'new_goods': new_goods,
               'ocount': ocount,
               'pagenums': pagenums}

    return render(request, 'duser/list.html', context)


def show_count(request):
    ocount = OrderInfo.objects.all().count()

    return JsonResponse({'ocount': ocount})


# 商品列表 超链接调用
def get_list(request):
    # 需要什么参数信息
    # 需要返回什么 页码范围 商品列表
    dic = request.GET
    type_id = int(dic.get('type_id'))
    page_id = int(dic.get('page_id'))
    print(type_id, page_id)

    # 获取分类数据
    typeinfo = TypeInfo.objects.get(pk=type_id)
    goods_all = typeinfo.goodsinfo_set.order_by('-id')
    paginator = Paginator(goods_all, 5)

    # 页码范围限定
    page_index = int(page_id)
    if page_index <= 0:
        page_index = 1
    if page_index >= paginator.num_pages:
        page_index = paginator.num_pages

    page = paginator.page(page_index)
    goods_list = page.object_list

    prange = paginator.page_range
    if paginator.num_pages > 5:
        if page_index <= 2:
            prange = range(1, 6)

        elif page_index >= paginator.num_pages - 1:

            prange = range(paginator.num_pages - 4, paginator.num_pages + 1)
        else:
            prange = range(page_index - 2, page_index + 3)

    prange = list(prange)

    # 将模型集合序列化
    serializer = GoodsSerializer(goods_list, many=True)
    # 将序列化后的数据包装为JSON响应对象
    data = {'model_list': serializer.data, 'page_range': prange}
    js_data = JSONResponse(data)
    return js_data  # JSONResponse


@logged
def cart(request):
    #  获取购物车订单信息
    #
    orders = OrderInfo.objects.all()
    context = {'orders': orders}
    return render(request, 'duser/cart.html', context)


# 添加到购物车
@logged
def add_goods(request):
    # 用户id uid
    # 商品id gid
    # 数量 gcount
    # 用户id 和商品id一致则只改变数量 否则 新增一条数据

    uid = request.session['uid']
    uid = UserInfo.objects.get(pk=uid)

    gid = request.GET.get('gid')
    gid = Goodsinfo.objects.get(pk=gid)

    gcount = request.GET.get('gcount')
    order = OrderInfo.objects.filter(user=uid, goods_id=gid)

    if order:
        order[0].goods_count += int(gcount)
        order[0].save()
    else:
        new_order = OrderInfo()
        new_order.user = uid
        new_order.goods_id = gid
        new_order.goods_count = gcount
        new_order.save()

    return JsonResponse({'isok': 1})


# 从购物车删除
@logged
def del_goods(request):
    # 商品id
    gid = request.GET.get('gid')
    order = OrderInfo.objects.get(goods_id_id=gid)
    order.delete()
    return JsonResponse({'isok': 1})


# # 提交订单 生成订单
# @logged
# def place_order(request):
#     return JsonResponse({'isok': 1})


# 去结算
# 选中商品的gid
@logged
def to_jiesuan(request):
    # 商品编号
    dic = request.POST
    gids = dic.getlist('gid')  # list
    # 订单用户
    user_id = request.session.get('uid')
    user = UserInfo.objects.get(pk=user_id)
    orders = OrderInfo.objects.filter(pk__in=gids)
    context = {'user': user, 'orders': orders}
    return render(request, 'duser/place_order.html', context)


# 选择结算方式等，然后提交订单
@logged
def submit_order(request):
    sid = transaction.savepoint()
    try:
        dic = request.POST
        oids = dic.getlist('oid')
        address = dic.get('address')

        uid = request.session.get('uid')
        buyer = BuyInfo()  # 构造订单
        # 购买编号
        buyer.buyid = datetime.now().strftime('%y%m%d%H%M%S%f%') + str(uid)

        # 购买用户
        buyer.buyuser = UserInfo.objects.get(pk=uid)
        # 订单总价
        buyer.buytotoal = 0
        # 收货地址
        buyer.buyaddress = address
        buyer.save()
        orders = OrderInfo.objects.filter(pk__in=oids)
        totol = 0

        for order in orders:
            if order.goods_count > order.goods_id.gkucun:
                transaction.savepoint_rollback(sid)
                return redirect('/cart/')
            else:
                buydetail = BuyDetailInfo()
                buydetail.buy = buyer
                buydetail.goods = order.goods_id
                buydetail.count = order.goods_count
                buydetail.price = order.goods_id.gprice
                buydetail.save()

                # 修改库存数量
                goods = order.goods_id
                goods.gkucun -= order.goods_count
                goods.save()
                # 计算总价
                totol += order.goods_count * order.goods_id.gprice
                # 删除购物车
                order.delete()
        buyer.buytotoal = totol
        buyer.save()
        transaction.savepoint_commit(sid)
        return redirect('/user/user_center_order/')
    except Exception:
        transaction.savepoint_rollback(sid)
        return redirect('/cart/')


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


class MySearchView(SearchView):
    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        context['title'] = '搜索结果'
        # context['cart'] = '1'
        # context['isleft'] = '0'
        return context

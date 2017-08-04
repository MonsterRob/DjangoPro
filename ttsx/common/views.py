from django.shortcuts import render
from .models import TypeInfo, Goodsinfo
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from .serializer import GoodsSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json


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
    class_ = ['fruit', 'seafood', 'meet', 'egg', 'vegetables', 'ice']
    context = {'list_': list_, 'class_': class_}

    return render(request, 'duser/index.html', context)


# 商品详情页
def detail(request, goods_id):
    try:
        goods = Goodsinfo.objects.get(pk=goods_id)

        context = {'goods': goods, 'kucun': goods.gkucun}
        return render(request, 'duser/detail.html', context)
    except Exception:
        return render(request, '404.html')


# 商品列表页
def more_goods(request, type_id, page_id):
    print(type_id, page_id)
    typeinfo = TypeInfo.objects.get(pk=type_id)
    goods_list = typeinfo.goodsinfo_set.order_by('-id')
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

    context = {'typeinfo': typeinfo,
               'page': page,
               'prange': prange}

    return render(request, 'duser/list.html', context)


def get_list(request):
    # 需要什么参数信息
    # 需要返回什么 页码范围 商品列表
    dic = request.GET
    type_id = int(dic.get('type_id'))
    page_id = int(dic.get('page_id'))

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

    # 将模型集合序列化
    serializer = GoodsSerializer(goods_list, many=True)
    # 将序列化后的数据包装为JSON响应对象
    js_data = JSONResponse(serializer.data)

    return js_data  # JSONResponse


def get_prange(request):
    # 需要什么参数信息
    # 需要返回什么 页码范围

    dic = request.GET

    type_id = int(dic.get('type_id'))
    page_id = int(dic.get('page_id'))

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

    prange = paginator.page_range
    if paginator.num_pages > 5:
        if page_index <= 2:
            prange = range(1, 6)

        elif page_index >= paginator.num_pages - 1:

            prange = range(paginator.num_pages - 4, paginator.num_pages + 1)
        else:
            prange = range(page_index - 2, page_index + 3)

    prange = list(prange)
    content = {
        'index': page_index,
        'top': prange.pop(),
        'limit': paginator.num_pages
    }

    return JsonResponse(content)


# 购物车页
def cart(request):
    return render(request, 'duser/cart.html')


# 提交订单页
def place_order(request):
    return render(request, 'duser/place_order.html')


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

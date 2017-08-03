from django.shortcuts import render
from .models import TypeInfo, Goodsinfo
from django.core.paginator import Paginator
from django.http import JsonResponse


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
    goods = Goodsinfo.objects.filter(id=goods_id)
    context = {'goods': goods[0]}
    return render(request, 'duser/detail.html', context)


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


def list_data(request, type_id, page_id):
    typeinfo = TypeInfo.objects.get(pk=type_id)

    goods_list = typeinfo.goodsinfo_set.order_by('-id')
    paginator = Paginator(goods_list, 5)
    typeinfo = {'ttitle': typeinfo.ttitle
                }

    return JsonResponse({'key': 'value', 'typeinfo': typeinfo})


# 购物车页
def cart(request):
    return render(request, 'duser/cart.html')


# 提交订单页
def place_order(request):
    return render(request, 'duser/place_order.html')

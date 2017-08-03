from django.shortcuts import render


# Create your views here.
# 全局首页
def index(request):
    return render(request, 'duser/index.html')


# 商品详情页
def detail(request):
    return render(request, 'duser/detail.html')


# 商品列表页
def more_goods(request):
    return render(request, 'duser/list.html')


# 购物车页
def cart(request):
    return render(request, 'duser/cart.html')


# 提交订单页
def place_order(request):
    return render(request, 'duser/place_order.html')

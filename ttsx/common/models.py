from django.db import models
from tinymce.models import HTMLField
from duser.models import UserInfo


class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle


class Goodsinfo(models.Model):
    gtitle = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='goods')
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    isDelete = models.BooleanField(default=False)
    gunit = models.CharField(max_length=20, default='500g')
    gclick = models.IntegerField()
    gjianjie = models.CharField(max_length=200)
    gkucun = models.IntegerField()
    gcontent = HTMLField()
    gtype = models.ForeignKey(TypeInfo)

    def __str__(self):
        return self.gtitle


class OrderInfo(models.Model):
    user = models.ForeignKey(UserInfo)
    goods_id = models.ForeignKey(Goodsinfo)
    goods_count = models.IntegerField(default=0)


# 购买订单信息
class BuyInfo(models.Model):
    # 购买编号
    buyid = models.CharField(max_length=30, primary_key=True)
    # 购买用户
    buyuser = models.ForeignKey(UserInfo)
    # 下单日期
    buydate = models.DateTimeField(auto_now_add=True)  # 不需要赋值
    # 是否付款
    buyispay = models.BooleanField(default=False)
    # 订单总价
    buytotoal = models.DecimalField(max_digits=6, decimal_places=2)
    # 收货地址
    buyaddress = models.CharField(max_length=150)


# 单个商品的信息
class BuyDetailInfo(models.Model):
    # 商品
    goods = models.ForeignKey(Goodsinfo)
    # 购买
    buy = models.ForeignKey(BuyInfo)
    # 单价
    price = models.DecimalField(max_digits=5, decimal_places=2)
    # 数量
    count = models.IntegerField()

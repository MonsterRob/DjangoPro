from django.conf.urls import url
from . import views

app_name = 'common'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^more_goods(\d+)_(\d+)_(\d+)/$', views.more_goods, name='more_goods'),
    url(r'^detail(\d+)/$', views.detail, name='detail'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^place_order/$', views.place_order, name='place_order'),
    url(r'^get_list/$', views.get_list, name='get_list'),
    url(r'^get_prange/$', views.get_prange, name='get_prange'),
    url(r'^search/$', views.MySearchView.as_view(), name='search_view'),
    url(r'^add_goods/$', views.add_goods, name='add_goods'),
    url(r'^del_goods/$', views.del_goods, name='del_goods')

]

from django.conf.urls import url
from . import views

app_name = 'common'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^more_goods(\d+)_(\d+)_(\d+)/$', views.more_goods, name='more_goods'),
    url(r'^detail(\d+)/$', views.detail, name='detail'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^get_list/$', views.get_list, name='get_list'),
    url(r'^search/$', views.MySearchView.as_view(), name='search_view'),
    url(r'^add_goods/$', views.add_goods, name='add_goods'),
    url(r'^del_goods/$', views.del_goods, name='del_goods'),
    url(r'^to_jiesuan/$', views.to_jiesuan, name='to_jiesuan'),
    url(r'^submit_order/$', views.submit_order, name='submit_order'),
    url(r'^show_count/$', views.show_count, name='show_count')

]

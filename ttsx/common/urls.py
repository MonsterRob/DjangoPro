from django.conf.urls import url
from . import views
app_name = 'common'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail(\d+)/$', views.detail, name='detail'),
    url(r'^more_goods(\d+)_(\d+)/$', views.more_goods, name='more_goods'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^place_order/$', views.place_order, name='place_order'),
    url(r'^get_list/$', views.get_list, name='get_list'),
    url(r'^get_prange/$', views.get_prange, name='get_prange')

]

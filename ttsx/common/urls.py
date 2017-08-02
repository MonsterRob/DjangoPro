from django.conf.urls import url
from . import views
app_name = 'common'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/$', views.detail, name='detail'),
    url(r'^more_goods/$', views.more_goods, name='more_goods')
]

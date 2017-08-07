from django.conf.urls import url
from . import views

app_name = 'duser'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^check_name/$', views.check_name, name='check_name'),
    url(r'^check_login/$', views.check_login, name='check_login'),
    url(r'^register_in/$', views.register_in, name='register_in'),
    url(r'^user_center_info/$', views.user_center_info, name='user_center_info'),
    url(r'^user_center_order/$', views.user_center_order, name='user_center_order'),
    url(r'^user_center_site/$', views.user_center_site, name='user_center_site'),
    url(r'^parent/$', views.parent, name='parent'),
    url(r'^sons/$', views.sons, name='sons'),
    url(r'^change_site/$', views.change_site, name='change_site')

]

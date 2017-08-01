from django.conf.urls import url
from . import views

app_name = 'duser'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^check_name/$', views.check_name, name='check_name'),
    url(r'^check_login/$', views.check_login, name='check_login'),
    url(r'^register_in/$', views.register_in, name='register_in'),
]

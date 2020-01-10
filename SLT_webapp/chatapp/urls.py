from django.urls import path, include
from django.conf.urls import url
from . import views as views

app_name = 'cahtapp'
urlpatterns = [
    url(r'^view_users', views.view_users),
    url(r'^save_msg', views.save_msg),
    url(r'^get_chat', views.get_chat),
    url(r'^view_msg', views.view_msg),
    url(r'^index', views.index, name='index'),
]







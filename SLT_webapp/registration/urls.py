from django.urls import path, include
from . import views as views

app_name = 'registration'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('new-user/', views.new_user, name='new-user'),
    path('<str:username>/new-profile/', views.new_profile, name='new-profile'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('game/', views.game, name='game'),
    path('make-new-card/', views.make_new_card, name='make-new-card'),
    path('card-check/', views.card_check, name='card-check'),
    path('success/', views.success, name='success'),
    path('info/', views.info, name='info'),
]

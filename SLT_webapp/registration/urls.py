from django.urls import path, include
from . import views as views

app_name = 'registration'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('new-user/', views.new_user, name='new-user'),
    path('<str:username>/new-profile/', views.new_profile, name='new-profile'),
    path('<str:username>/new-profile-parent/', views.new_profile_parent, name='new-profile-parent'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('game/', views.game, name='game'),
    path('make-new-card/', views.make_new_card, name='make-new-card'),
    path('card-check/', views.card_check, name='card-check'),
    path('success/', views.success, name='success'),
    path('info/', views.info, name='info'),
    path('add-friend/', views.add_friend, name='add-friend'),
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/<int:message_id>/', views.view_message, name='view-message'),
    path('inbox/delete/<int:message_id>/', views.delete_message, name='delete-message'),
    path('inbox/new-message/', views.new_message, name='new-message'),
    path('active-games/', views.active_games, name='active-games'),
    path('exit/', views.exit_game, name='exit'),
    path('total-time-son/', views.total_time_son, name='total-time-son'),
    path('report-menu/', views.reports_menu, name='reports-menu'),
]

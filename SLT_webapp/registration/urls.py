from __future__ import absolute_import, unicode_literals
from django.urls import path, include
from . import views as views
from django.conf.urls import url

app_name = 'registration'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('new-user/', views.new_user, name='new-user'),
    path('<str:username>/new-profile/', views.new_profile, name='new-profile'),
    path('<str:username>/new-profile-parent/', views.new_profile_parent, name='new-profile-parent'),
    path('profile/', views.profile, name='profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete-notification'),
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
    path('send-game/', views.send_game, name='send-game'),
    path('total-time-son/', views.total_time_son, name='total-time-son'),
    url(
        regex=r'^chat$',
        view=views.UserListView.as_view(),
        name='user_list'
    ),
    path('report-menu/', views.reports_menu, name='reports-menu'),
    path('report-menu/details-of-users', views.reports_users, name='details-of-users'),
    path('/reports-menu/avg-points/', views.avg_points, name='avg-points'),
    path('rank-game/', views.rank_game, name='rank-game'),
    path('rank-success/', views.rank_success, name='rank-success'),
    path('/reports-menu/rank-for-admin/', views.rank_for_admin, name='rank-for-admin'),
    #path('active-users/', views.active_users_page, name='active-users'),
    path('report-user/', views.report_user, name='report-user'),
    path('/reports-menu-users/active-users/', views.active_users_page, name='active-users'),
    path('/reports-menu-users/', views.reports_menu_users, name='reports-menu-users'),
    path('/success-message/', views.success_message, name='success-message'),
    path('/lottery/', views.lottery_for_tournament, name='lottery'),
    path('/parent-list/', views.parent_list, name='parent-list'),
    path('/level-of-son/', views.level_of_son, name='level-of-son'),
    path('/success-level/', views.success_level, name='success-level'),
    path('/invite-friend/', views.invite_friend, name='invite-friend'),
    path('/success-invite/', views.success_invite, name='success-invite'),
    path('/suspend-users/', views.suspend_users, name='suspend-users'),
    path('/game-sessions-report/', views.game_sessions_report, name='game-sessions-report'),
    path('/limit-son/', views.limit_son, name='limit-son'),
]

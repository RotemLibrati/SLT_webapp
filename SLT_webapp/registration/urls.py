from django.urls import path
from . import views

app_name = 'registration'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/', views.profile, name='profile'),
    path('<int:pk>/details/', views.DetailView.as_view(), name='details'),
    path('<int:user_id>/make-new-card/', views.make_new_card, name='make-new-card'),
    path('<int:user_id>/card-check/', views.card_check, name='card-check'),
    path('<int:user_id>/success/', views.success, name='success'),
    path('<int:user_id>/game/', views.game, name='game'),
    path('new-user/', views.new_user, name='new-user'),
    path('new-user/<str:username>', views.new_profile, name='new-profile'),
]
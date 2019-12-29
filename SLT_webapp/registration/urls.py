from django.urls import path
from . import views

app_name = 'registration'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/', views.profile, name='profile'),
    path('<int:pk>/details/', views.DetailView.as_view(), name='details'),
]
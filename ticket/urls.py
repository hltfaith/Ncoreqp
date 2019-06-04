from django.urls import path
from . import views

app_name = 'ticket'  # 一定要写这一行，否则html中会报错 'account' is not a registered namespace

urlpatterns = [
    path('', views.login, name='user_login'),
    path('login/', views.login, name='user_login'),
    path('logout/', views.logout),
]
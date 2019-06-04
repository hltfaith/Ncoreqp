"""Ncoreqp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from ticket import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ticket.urls')),

    path('index/', views.index),
    path('cxcp1/', views.cxcp1),
    path('cxcp2/', views.cxcp2),
    path('cxcp3/', views.cxcp3),
    path('cxcp3/', views.cxcp3),

    path('setmail/', views.setmail),
    path('listmail/', views.listmail),
    path('mailIndex/', views.mailIndex),
    path('mailIndex2/', views.mailIndex2),
    path('ticket_list/', views.ticket_list),
    path('my_order/', views.my_order),
    path('airticket_change/', views.airticket_change),
    path('setmail/', views.setmail),

]

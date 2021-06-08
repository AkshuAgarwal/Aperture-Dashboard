from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('invite', views.invite, name='invite'),
    path('support', views.support, name='support'),
    path('login', views.login, name='login'),
    path('callback', views.callback, name='callback'),
    path('dashboard', views.dashboard, name='dashboard'),
]